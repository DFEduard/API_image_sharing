API FOR AN IMAGE SHARING APP


venv - virtual environment (must be activated)

-> Activate the environment:
	- open Command Prompt
	- type: cd pathToTheApp/venv/Scripts then hit enter
	- type: activate

You should see (venv) before the path of the directory.

-> Run the app:
	- with the environment activated "cd" to where is run.py
	- type: python3 run.py (use python 3)

All links:
	URL: http://127.0.0.1:5000/registration 			| Method: POST		| Requier: N/A
	URL: http://127.0.0.1:5000/login				| Method: GET		| Require: Basic Auth (username= user's email, password = pass) 
	URL: http://127.0.0.1:5000/get-api-token/publicIdOfTheUser_Here	| Method: GET		| Require: Public id , Authentication
	URL: http://127.0.0.1:5000/users				| Method: GET		| Require: User's token
	URL: http://127.0.0.1:5000/user-follow/aUserId_Here		| Method: PUT		| Require: User's token
	URL: http://127.0.0.1:5000/user-unfollow/aUserId_Here		| Method: PUT		| Require: User's token
	URL: http://127.0.0.1:5000/posts/				| Method: GET		| Require: User's token
	URL: http://127.0.0.1:5000/post-create				| Method: POST		| Require: User's token
	URL: http://127.0.0.1:5000/post-like/aPostId_Here		| Method: PUT		| Require: User's token
	URL: http://127.0.0.1:5000/images				| Method: GET		| Require: User's token

				MORE INFO 
##############################################################################
 Create new account

	URL: http://127.0.0.1:5000/registration
	Method: POST

	Json format (copy and paste and change valueHere with your data)

			"first_name": "valueHere",
			"last_name":"valueHere",
			"email":"valueHere",
			"password": "valueHere"

	Return json format
		"message":"Account has been created!",
		"public_id": "user's public id"
		"api-token": "user's token"

NOTE
	- public id can be used to recover the api-token
	- api-token must be used to access all the functionalities of this API and to identify the user

##############################################################################
 Login

	URL: http://127.0.0.1:5000/login
	Method: GET

	Authorization 
			Type: Basic Auth
			Username: user's email
			Password: user's password

	Return json format
		"message":"returned message here",
		"public_id":"user's public id"

NOTE
	- the only purpose of this page is to get the public_id in case you don't remember
	- the public_id can be used to recover the api-token

##############################################################################
Recover api-token of a user

	URL: http://127.0.0.1:5000/get-api-token/<public_id>
	Method: GET
	
	Authorization 
			Type: Basic Auth
			Username: the user's email 
			Password: the user's password 
	
	Return json format:
		"message":"Successfully authenticated!",
		"token": "user's token here",
		"name": "user's name"

NOTE: 
	- the token must be used to access the functionalities of this API and to identify the user

##############################################################################
List of all users
	

	URL: http://127.0.0.1:5000/users
	Method: GET
	Token -> KEY: api-token 
	
	
	Return json format:
		"users": [
    				{
      				"id": -,
      				"first_name": "-",
      				"last_name": "-",
      				"email": "-",
      				"posts": "-",
      				"followers": "-",
      				"following": "-"
    				},
				{
					user2 info
				}
				...

NOTE: 
	- List of all registered users will be returned 
	- You can see the user's info plus the number of the posts, followers and following

##############################################################################
Follow/Unfollow a user
	
Follow
	URL: http://127.0.0.1:5000/user-follow/<user_id>
Unfollow
	URL: http://127.0.0.1:5000/user-unfollow/<user_id>
	Method: PUT
	Token -> KEY: api-token | Values: user's token 
	(Without the token this page cannot be accessed. The token is taken from headers)
	
	
	Return json format:
		"message": "returned message"

NOTE: 
	- You can follow and unfollow other users.
	- Use the user's id not the public id
	- List all users to see the user's id 
	- You cannot follow/unfollow your own account

##############################################################################
Create a post
	
Follow
	URL: http://127.0.0.1:5000/post-create
	Method: POST
	Token -> KEY: api-token | Values: user's token 
	(Without the token this page cannot be accessed. The token is taken from headers)
	
	
	Json format (copy and paste and change valueHere with your data)

			"caption": "textHere",
			"image_file":"URLhere"
	
	Return json format:
		"message": "returned message here"

NOTE: 
	- Caption is limited to 100 chars 
	- The image will be downloaded to /static directory if is possible

##############################################################################
Create a post
	
Follow
	URL: http://127.0.0.1:5000/post-create
	Method: POST
	Token -> KEY: api-token | Values: user's token 
	(Without the token this page cannot be accessed. The token is taken from headers)
	
	
	Json format (copy and paste and change valueHere with your data)

			"caption": "textHere",
			"image_file":"URLhere"
	
	Return json format:
		"message": "returned message here"

NOTE: 
	- Caption is limited to 100 chars 
	- The image will be downloaded to /static directory if is possible

##############################################################################
List of all posts
	
Follow
	URL: http://127.0.0.1:5000/posts
	Method: GET
	Token -> KEY: api-token | Values: user's token 
	(Without the token this page cannot be accessed. The token is taken from headers)
	
	
	
	Return json format:
		"posts": [
  			{
      			"id": "-",
      			"caption": "-",
      			"image_file": "-",
      			"date_posted": "-",
      			"author": "-",
      			"likes": "-"
    			},
			{
			Second post...
			}	
			...
			]

NOTE: 
	- Posts are ordered by likes (most likes first)

##############################################################################
Post like
	
Follow
	URL: http://127.0.0.1:5000/post-like/<post_id>
	Method: PUT
	Token -> KEY: api-token | Values: user's token 
	(Without the token this page cannot be accessed. The token is taken from headers)
	
	
	
	Return json format:
		"message": "returned message here"

NOTE: 
	- Use post_id (list all posts to see all the ids of the registered posts)
	- A user can like his own post as well

##############################################################################
List images
	

	URL: http://127.0.0.1:5000/images
	Method: GET
	Token -> KEY: api-token | Values: user's token 
	(Without the token this page cannot be accessed. The token is taken from headers)
	
	
	
	Return json format:
		"message": "returned message here"
		"Images": [
    				{
      				"image_file": "/static/8wuiPP5f.jpg"
    				},
				{
				"image_file": "URL here, if not downloaded"
				},
				...
			  ]

NOTE: 
	- List of images for the current user
	- Most recent first
	- Limited to the user's following
	
	