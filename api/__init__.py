# Author: Floreint-Eduard Decu
# Date: July 2020

# All imports necessary to create a basic flask app 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


# Instantiate flask application
app = Flask(__name__)

# I usualy hide the secret key on the operating system environmnet or into a json file in another location 
# For this demo I will leave it as it is now 
app.config['SECRET KEY'] = '4b435858fe444cbb9fe84b5f246e6540'

# Configure the database URI that will be used for the connection
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///apidata.db"

# Configure json to prevent to sort data alphabetically
# (makes no sense when data is returned alphabetically, without sorting is easy readable) 
app.config['JSON_SORT_KEYS'] = False

# Initialise SQLAlchemy (ORM DATABASE)
db = SQLAlchemy(app)

# Initial Bcrypt (used to encrypt and decrypt data)
bcrypt = Bcrypt(app)


# If routes will be imported before to initialise 'app', 'db', and 'bcrypt' an error (ImportError) will be thrown 
# This is happening because 'routes' must import that variables as well
# If the variables are initialized before 'routes' is imported, the 'routes' script can find the variables and import them
from api import routes