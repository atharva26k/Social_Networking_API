from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

from .serializers import UserSignupSerializer, UserLoginSerializer
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer

# Create your views here.


class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = []


class UserLogin(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchPagination(PageNumberPagination):
    page_size = 10


class UserSearch(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = UserSearchPagination

    def get_queryset(self):
        find_users = self.request.query_params.get('find', '')
        if '@' in find_users:
            return User.objects.filter(email=find_users)
        else:
            return User.objects.filter(Q(name__icontains=find_users) | Q(email__icontains=find_users))


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(email=to_user_id)
        from_user = request.user

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        if FriendRequest.objects.filter(from_user=from_user, created_at__gte=one_minute_ago).count() >= 3:
            return Response({'error': 'Cannot send more then 3 frined requests in a minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()

        return Response({'status': 'Friend request sent!'}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        action = request.data.get('action')
        friend_req = FriendRequest.objects.get(
            id=request_id, to_user=request.user)

        if action == 'accept':
            friend_req.is_accepted = True
            friend_req.save()
            return Response({'status': 'Friend request accepted'}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_req.delete()
            return Response({'status': 'Friend request rejected'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)


class FriendsList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            Q(sent_requests__to_user=self.request.user, sent_requests__is_accepted=True) |
            Q(received_requests__from_user=self.request.user,
              received_requests__is_accepted=True)
        ).distinct()


class PendingFriendRequests(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, is_accepted=False)
