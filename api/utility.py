# Author: Floreint-Eduard Decu
# Date: July 2020

import re # Import regular expresion to check emails
import random
import os
from PIL import Image
from api.models import Post 
import urllib.request
from api import app
from flask import request

# Regular expresion 
# Define a search pattern 
regex = '^([0-9a-zA-Z]([-\\.\\w]*[0-9a-zA-Z])*@([0-9a-zA-Z][-\\w]*[0-9a-zA-Z]\\.)+[a-zA-Z]{2,9})$'

# Used to valided emails
def check_email(email):
    if (re.search(regex,email)):
        return True
    else:
        return False

# Used to sort a Post list based on the date_posted
def sort_list(Post):
    return Post.date_posted

# Download an image from url to /static directory
def save_image(url):

    img_name = random_names(8) + '.jpg'

    

    # Download the image from url 
    try:
        path = os.path.join(app.root_path, 'static/',img_name)
        urllib.request.urlretrieve(url, path)
        return str(img_name)
    except: # Return url when error occurs
        return str(url)

        
# Used to create random names
# Length must be provided
def random_names(length):                                                           
                                                                                    
    alphabet = "abcdefghijklmnopqrstuvwxyz"                                         
    upper_alphabet = alphabet.upper()                                               
    passwordList = []                                                               
                                                                                    
    for i in range(int(length)//3):                                                 
        passwordList.append(alphabet[random.randrange(len(alphabet))])              
        passwordList.append(upper_alphabet[random.randrange(len(upper_alphabet))])  
        passwordList.append(str(random.randrange(10)))                              
    for i in range(length-len(passwordList)):                                       
        passwordList.append(alphabet[random.randrange(len(alphabet))])              
                                                                                    
    random.shuffle(passwordList)                                                    
    password = "".join(passwordList)                                                
                                                                                    
    return password                                                                 