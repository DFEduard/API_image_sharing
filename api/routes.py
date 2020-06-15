# Author: Floreint-Eduard Decu
# Date: July 2020


import uuid # Used to create public id for users (much safer with public id)
import jwt # Used to create a token
import datetime
from flask import request, jsonify, make_response, redirect, url_for # Flask imports necessary to build this API
from api import app, db, bcrypt # These importes variables will be create in __inti__.py
from functools import wraps # Used to create decorators 
from api.models import User, Post # Database models. (ORM database)
from api.utility import check_email, sort_list, save_image # Helping functions
from sqlalchemy.sql import text # Used to create raw SQL statements 


# Decorator used to check the tokens, to login a user, and to check the current user 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for api keyword and get the token 
        if 'api-token' in request.headers:
            token = request.headers['api-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the passed token 
            data = jwt.decode(token, app.config['SECRET KEY'])
            # Use the public_id saved into the token to get the user's data from database
            # This is going to be the current user
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message':'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


#Users can register by accessing this page domain name or ip address/registration
@app.route('/registration', methods=['POST'])
def register_user():

    # Get data from request (user's details)
    data = request.get_json()

    # Encrypt the user's password
    hash_password = bcrypt.generate_password_hash(data['password'])

    # Create public id for the user
    public_user_id = str(uuid.uuid4())

    # Check to see if the email has been already used by another user
    email_exists = db.session.query(User.email).filter_by(email=data['email']).scalar()

    # Check for invalid email 
    if check_email(data['email']) == False:
        return jsonify({'message':'Invalid email!'})
    else:
        #  Check to see if the email provied is not used by another user 
        if not email_exists:

            # Create user object 
            new_user = User(
                public_id = public_user_id,
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password = hash_password
            )

            # Add the user to database 
            db.session.add(new_user)
            db.session.commit()

            # Create a token for the registered user 
            token = jwt.encode({'public_id': new_user.public_id}, app.config['SECRET KEY'])

            # Return the created token and public id to the user 
            # Note: All users must use their public id and token to access and use this api 
            return jsonify({'message':'Acount has been created!',
                            'public_id': new_user.public_id,
                            'api-token':token.decode('UTF-8')})
        else:
            return jsonify({'message':'This email: ' + data['email'] + ' is already registered'})


# Registered users must login before to use the api
# Public ip address will be displayed (used to access other pages)
@app.route('/login')
def login():
    # Get authentication credentials 
    auth = request.authorization

    # Check for authentication data
    # the username in this case is the user's email
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401, {'WWW-Authenticate': 'Basic releam="Login required!"'})

    # Get user data from database
    user = User.query.filter_by(email=auth.username).first()

    # Check for empty result 
    if not user:
        return make_response('Could not verify',401, {'WWW-Authenticate': 'Basic releam="Login required!"'})

    # Check the user's password 
    if bcrypt.check_password_hash(user.password, auth.password):
        return jsonify({'message':'Succesfully login!',
                        'public_id': str(user.public_id)})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    

# Show a list of all registered users
@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):

    # Get all users from database
    users = User.query.all()
    # Create empty list to store all the users
    output = []

    for u in users:
        # Create dictionary to add into the output list
        user_data = {}
        # Store user data in json format 
        user_data['id'] = u.id
        user_data['first_name'] = u.first_name
        user_data['last_name'] = u.last_name
        user_data['email'] = u.email
        user_data['posts'] = str(len(u.posts))
        user_data['followers'] = str(len(u.followed_by))
        user_data['following'] = str(u.following.count())
        # Add dictionary into the list 
        output.append(user_data)

    # Return all users from database
    return jsonify({'users': output})
    

# Current user can follow any user by passing the user's id 
@app.route('/user-follow/<user_id>', methods=['PUT'])
@token_required
def follow_user(current_user, user_id):

     # Check if parameter is different from the current user id (preventing the current user to follow its own account)
    if str(current_user.id) != user_id:

        # Get the user's data from database
        user_followed = User.query.filter_by(id=user_id).first()

        # Check if the current user already follow the user
        is_followed = current_user in user_followed.followed_by

        # Check the result
        if is_followed == True:
            # Return a message to notify the user that is already following the chose user 
            return({'message': 'You already follow ' + user_followed.first_name + ' '+ user_followed.last_name})
        else:
            # Follow the chose user
            user_followed.followed_by.append(current_user)
            db.session.commit()

    # Return feedbacks 
            return jsonify({'message': 'You follow ' + user_followed.first_name + ' '+ user_followed.last_name})

    elif str(current_user.id) == user_id:
        return jsonify({'message': 'You can\'t follow / unfollow yourself'})



# Current user can unfollow a user by passing the user's id as parameter to the URL
@app.route('/user-unfollow/<user_id>', methods=['PUT'])
@token_required
def unfollow_user(current_user, user_id):

    # Check if parameter is different from the current user id (preventing the current user to unfollow its own account)
    if str(current_user.id) != user_id:

        # Get the user that should be followed by the current user
        user_followed = User.query.filter_by(id=user_id).first()

        # Check if the current user already follow the user
        is_followed = current_user in user_followed.followed_by

        # Check the result 
        if is_followed == True:

            # Unfollow the chosen user
            user_followed.followed_by.remove(current_user)
            db.session.commit()

    # Return feedbacks 
            return({'message': 'You unfollow ' + user_followed.first_name + ' '+ user_followed.last_name})

        else:
            return jsonify({'message': 'You don\'t follow ' + user_followed.first_name + ' '+ user_followed.last_name})

    elif str(current_user.id) == user_id:
        return jsonify({'message': 'You can\'t follow / unfollow yourself'})


# Returns images for the current user -> most recenet first limited to users following 
@app.route('/images', methods=['GET'])
@token_required
def current_user_images(current_user):

    # Store all posts posted by the users that are followed by the current user 
    posts = []
    posts.clear()
    try:
        # Iterate through all users that are followed by the current user 
        for followed in current_user.following:
            # Iterate through all the posts posted by the users followed by the current user
            for post in followed.posts:
                # Store the posts
                posts.append(post)
        
        # Sort the posts in desc. most recent first
        sort_posts = sorted(posts, key=sort_list, reverse=True)

        # Clear the list of unsorted posts 
        posts.clear()

        # Iterate through all the sorted posts 
        for post in sort_posts:

            # Create dictionary
            post_data ={}
            # Store the image url 
            img_url = post.image_file

            # If URL contain http return the URL 
            if 'http' in img_url:
                post_data['image_file'] = img_url
            else: # Return the path of the image where has been saved
                post_data['image_file'] = url_for('static', filename=img_url)

            # Add dictionary to posts list 
            posts.append(post_data)

        # Return all posts posted by the users that are followed by the current user in desc. order (most recent first)
        return jsonify({'message':' Images are limited to users following (most recent first)','Images': posts})
    except:
        return jsonify({'messages': 'No image found!'})


# Show a list of all posts from all users
@app.route('/posts', methods=['GET'])
@token_required
def get_all_posts(current_user):

    
    # Get all posts from database
    #posts = Post.query.all()
    query = "SELECT post.*, COUNT(postlikes.user_id) as likes FROM post LEFT OUTER JOIN postlikes ON postlikes.post_id = post.id GROUP BY post.id ORDER BY likes DESC"
    posts = db.session.query(Post).from_statement(text(query)).all()

    # Initialise empty list
    output = []

    # Iterate through all posts
    for post in posts:
        # Create dictionary and add data
        post_data = {}
        post_data['id'] = str(post.id)
        post_data['caption'] = post.caption

        # Store the image url 
        img_url = post.image_file

        # If URL contain http return the URL 
        if 'http' in img_url:
            post_data['image_file'] = img_url
        else: # Return the path of the image where has been saved
            post_data['image_file'] = url_for('static', filename=img_url)
        
        post_data['date_posted'] = post.date_posted
        post_data['author'] = post.author.first_name + ' ' + post.author.last_name
        post_data['likes'] = str(len(post.likes))
        # Add current dictionary to the list 
        output.append(post_data)

    # Return all posts data 
    return jsonify({'posts': output})
    

# Create a post
@app.route('/post-create', methods=['POST'])
@token_required
def create_post(current_user):
    # Get data from request 
    data = request.get_json()
    # Check the length if the caption (caption is limited to 100 chars)
    if len(data['caption']) <= 100:
        post_image = save_image(url=data['image_file'])
        # Create post object 
        post = Post(caption=data['caption'], image_file=post_image, user_id=current_user.id)
        # Add to database
        db.session.add(post)
        db.session.commit()

    # Return feedbacks
        return jsonify({'message':'Post created!'})
    else:
        return jsonify({'message': 'Caption is limited to 100 chars'})


# Current user can like a post by passing the an id of recorded post 
@app.route('/post-like/<post_id>', methods=['PUT'])
@token_required
def like_post(current_user, post_id):

    # Get the chosen post from database
    post = Post.query.filter_by(id=post_id).first()

    # Check if post exist
    if post:

        # Check if the current user already liked the post 
        already_like = current_user in post.likes
        
        # If post is not liked by the current user save changes to database
        if already_like == False:

            # Associate the current user with the post (means the current user like the post )  
            post.likes.append(current_user)
            db.session.commit()

    # Return feedbacks 
            return jsonify({'message':'Post liked!', 'current_user': current_user.email})
        else:
            return jsonify({'message':'You already pressed like for this post', 'current_user': current_user.email})
    elif not post:
        return jsonify({'message':'No post found!'})
        


# Users can recover their token in case they forgot it.
# They must provide their public id address and to authenticate with their email and password
@app.route('/get-api-token/<public_id>', methods=['GET'])
def get_token(public_id):

    # Get authentication credentials 
    auth = request.authorization

    # Check for authentication data
    # the username in this case is the user's email
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401, {'WWW-Authenticate': 'Basic releam="Login required!"'})

    # Get the user's details from database
    user = User.query.filter_by(email=auth.username).first()

    # Check for empty result
    if not user:
        return make_response('Could not verify',401, {'WWW-Authenticate': 'Basic releam="Login required!"'})

    # Check to see if the public id of the user match with the one passed through the URL
    if user.public_id != public_id:
        return jsonify({'message':'Invalid public id!'})

    # Check the user's password
    if bcrypt.check_password_hash(user.password, auth.password):
        # Create token by using the user's public id address and the app secret key 
        token = jwt.encode({'public_id':user.public_id}, app.config['SECRET KEY'])
        return jsonify({'message':'Succesfully authenticate!', 
        'token': str(token.decode('UTF-8')),
        'name': str(user.first_name) +' '+ str(user.last_name[0])+'.'})
    
    

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})



