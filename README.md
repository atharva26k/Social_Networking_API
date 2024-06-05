Installation Steps:

1. Clone the repository to your local system or download the zip file and extract in a destination folder.

2. Create a virtual environment in the destination folder 
	- python -m venv virt
	
3. Activate the virtual environment

4. Install required packages using requirements.txt
	- pip install -r requirements.txt
	
5. Run the server with
	- python manage.py runserver

6. Goto URL localhost:8000 to check working status.

7. Open Postman and import the API collection to check all the endpoints and its uses.
	- File to import: Accuknox Social App.postman_collection.json
	- Can be viewed directly also in .json format in any text editor of your choice.

8. Test the endpoints in postman:
	- [POST] Create a user with /api/signup
	- [POST] Login with that user from /api/login/
	- [GET] Search other users with a keyword /api/search/
	- [POST] Send a friend request to another user with /api/friend-request/
	- [PUT] Accept/reject friend requests with /api/friend-request/
	- [GET] Tiew all friends with /api/friends/
	- [GET] View all pending requests with /api/pending-request/

8. Containerize the API with Docker by creating a docker container.
	- Configuration files: 
		a. Dockerfile
		b. docker-container.yml

9. If required, build the container and run the image with the commanddocker-compose
	- docker-compose up --build
	
