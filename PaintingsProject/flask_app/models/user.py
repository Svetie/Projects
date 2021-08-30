# user.py
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #************************************
    #   Validation
    #************************************
    @staticmethod
    def validate_registration( user ):
        is_valid = True
        # check if email exists

        # if fields are empty
        if not user['first_name']:
            flash("First name field is required")
            is_valid = False
        if not user['last_name']:
            flash("Last name field is required")
            is_valid = False
        if not user['email']:
            flash("Email field is required")
            is_valid = False
        if not user['password']:
            flash('Password field is requied')
            is_valid = False
        if not user['confirm_password']:
            flash('Confirm password field is requied')
            is_valid = False

        #length validation
        if(len(user['first_name']) <  2):
            flash('First name should be at least 2 letters long')
            is_valid = False
        if(len(user['last_name']) <  2):
            flash('Last name should be at least 2 letters long')
            is_valid = False
        if(len(user['password']) <  8):
            flash('Password should be at least 8 characters long')
            is_valid = False

        # compare passwords
        if user['password'] != user['confirm_password']:
            flash('Passwords do not match')
            is_valid = False

        # check if email matches required criterea
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email format!')
            is_valid = False

        return is_valid

    #************************************
    #   Save user
    #************************************
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now());"

        id = connectToMySQL('paintings_schema').query_db(query, data)
        return id

    #************************************
    #   Get user by email
    #************************************
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("paintings_schema").query_db(query, data)

        if len(results) < 1:
            return False
        return cls( results[0] )

    #************************************
    #   Get user by ID
    #************************************
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("paintings_schema").query_db(query, data)
        return cls( results[0] )