from django.urls import path
from .views import UserSignup, UserLogin, UserSearch, FriendRequestView, FriendsList, PendingFriendRequests 

urlpatterns = [
    path('signup/', UserSignup.as_view(), name='user-signup'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('search/', UserSearch.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friends/', FriendsList.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequests.as_view(), name='pending-requests'),
]