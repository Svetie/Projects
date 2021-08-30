# user.py
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

SCHEMA = 'users_groups_schema'
NAME_REGEX  = re.compile(r'^[a-zA-Z]+$')
PW_REGEX    = re.compile(r'^[a-zA-Z0-9]+$')
PW_HC_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,24}$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name  = data['last_name']
        self.email      = data['email']
        self.password   = data['password']
        self.phone      = data['phone']
        self.phone_alt  = data['phone_alt']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.address_id    = data['address_id']

        self.address = {
            # 'street1':  data['street1'],
            # 'street2':  data['street2'],
            # 'city':     data['city'],
            # 'state':    data['state'],
            # 'zipcode':  data['zipcode'],
            # 'country':  data['country']
        }

    @staticmethod
    def valid_login(user):
        login_valid = False
        pw_valid    = False
        length = len(user['email'])
        if ( length >= 3 and length <= 45 ):
            if EMAIL_REGEX.match(user['email']):
                login_valid = True
        length = len(user['password'])
        if ( length >= 8 and length <= 24 ):
            if PW_HC_REGEX.match(user['password']):
                pw_valid = True
        return login_valid and pw_valid

    @staticmethod
    def valid_new_user(user):
        fname_valid = False
        lname_valid = False
        email_valid = False
        pw_valid    = False
        ############--Login name
        length = len(user['email'])
        if ( length >= 5 and length <= 16 ):
            if EMAIL_REGEX.match(user['email']):
                login_valid = True
            else:
                flash('Email address must be a valid email address.', 'warning')
                print('Email address must be a valid email address.', 'warning')
        else:
            flash("Email address must be at least 5 characters and no more than 45 characters long.", 'warning')
            print("Email address must be at least 5 characters and no more than 45 characters long.", 'warning')
        ############--Password
        length = len(user['password'])
        if user['password'] == user['pw_verify'] :
            if ( length >= 8 and length <= 24 ):
                if PW_HC_REGEX.match(user['password']):
                    pw_valid = True
                else:
                    flash('Password must be alphanumeric plus standard characters only.', 'warning')
                    print('Password must be alphanumeric plus standard characters only.', 'warning')
            else:
                flash("Password must be at least 8 characters and no more than 24 characters long.", 'warning')
                print("Password must be at least 8 characters and no more than 24 characters long.", 'warning')
        else:
            flash('Passwords do not match!', 'error')
            print('Passwords do not match:', user['password'], user['pw_verify'])
        ##############--FIRST NAME
        length = len(user['first_name'])
        if ( length >= 3 and length <= 16 ):
            if NAME_REGEX.match(user['first_name']):
                fname_valid = True
                print('first name is valid')
            else:
                flash('First name must be letters only.', 'warning')
                print('First name must be letters only.', 'warning')
        else:
            flash("First name must be at least 3 characters and no more than 16 characters long.", 'warning')
            print("First name must be at least 3 characters and no more than 16 characters long.", 'warning')
        ##############--LAST NAME
        length = len(user['last_name'])
        if ( length >= 3 and length <= 32 ):
            if NAME_REGEX.match(user['last_name']):
                lname_valid = True
                print('last name is valid')
            else:
                flash('Last name must be letters only.', 'warning')
                print('Last name must be letters only.', 'warning')
        else:
            flash("Last name must be at least 3 characters and no more than 32 characters long.", 'warning')
            print("Last name must be at least 3 characters and no more than 32 characters long.", 'warning')
        ##############--EMAIL
        length = len(user['email'])
        if ( length >= 5 and length <= 48 ):
            if EMAIL_REGEX.match(user['email']):
                email_valid = True
                print('email is valid')
            else:
                flash('Email address is not valid.', 'error')
                print('Email address is not valid.', 'error')
        else:
            flash("Email address must be at least 5 characters and no more than 48 characters long.", 'warning')
            print("Email address must be at least 5 characters and no more than 48 characters long.", 'warning')
        print('combined valid states are:', fname_valid and lname_valid and email_valid and login_valid and pw_valid)
        return (fname_valid and lname_valid and email_valid and pw_valid)

    # get all users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(SCHEMA).query_db(query)
        entries = []
        for item in results:
            entries.append(cls(item))
        return entries

    #get all users at one address by ID
    @classmethod
    def get_all_with_addresses(cls):
        query = "SELECT * FROM users JOIN addresses ON address_id = addresses.id ORDER BY last_name ASC;"
        results = connectToMySQL(SCHEMA).query_db(query)
        entries = []
        for item in results:
            entries.append(cls(item))
        return entries

    # get one user by email
    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        results = connectToMySQL(SCHEMA).query_db(query, data)

        if results:
            return cls( results[0] )
        else:
            return results

    #get one user by ID
    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        results = connectToMySQL(SCHEMA).query_db(query, data)

        if results:
            return results[0]
        else:
            return results

    #get all users with a last name
    @classmethod
    def getby_lastname(cls, data):
        query = 'SELECT * FROM users WHERE last_name = %(last_name)s'
        results = connectToMySQL(SCHEMA).query_db(query, data)

        if results:
            return results[0]
        else:
            return results

    #add a user
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users ( email, password, first_name, last_name , phone, phone_alt, created_at, updated_at, address_id ) VALUES ( %(email)s, %(password)s, %(first_name)s, %(last_name)s, %(phone)s, %(phone_alt)s, NOW() , NOW(), %(address_id)s );"
        return connectToMySQL(SCHEMA).query_db(query, data)

    #update a user
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, phone = %(phone)s, phone_alt = %(phone_alt)s, updated_at=NOW() WHERE id =%(id)s"
        return connectToMySQL(SCHEMA).query_db(query, data)

    #delete a user
    @classmethod
    def remove_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(SCHEMA).query_db(query, data)

    #check for existing user by first and last name and email
    @classmethod
    def check_new(cls, data):
        query = "SELECT id FROM users WHERE (first_name = %(first_name)s AND last_name = %(last_name)s AND email = %(email)s);"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if results:
            return results[0]
        else:
            return results

    # add one address
    @classmethod
    def add_address(cls, data):
        query = "INSERT INTO addresses (street1, street2, city, state, zipcode, country, created_at, updated_at) VALUES (%(street1)s, %(street2)s, %(city)s, %(state)s,%(zipcode)s, %(country)s, now(), now());"
        return connectToMySQL(SCHEMA).query_db(query, data)

    # get one address by ID
    @classmethod
    def get_address(cls, data):
        query = 'SELECT * FROM addresses WHERE users.address_id = %(address_id)s'
        results = connectToMySQL(SCHEMA).query_db(query, data)

        if results:
            return results[0]
        else:
            return results

    # get all addresses
    @classmethod
    def get_all_addresses(cls):
        query = "SELECT * FROM addresses ORDER BY last_name ASC;"
        results = connectToMySQL(SCHEMA).query_db(query)
        entries = []
        for item in results:
            entries.append(cls(item))
        return entries

    # get all users at an address, is exact match by all address fields except country
    @classmethod
    def getby_address(cls, data):
        query = 'SELECT * FROM users JOIN addresses ON users.address_id = addresses.id WHERE addresses.street1 = %(street1)s AND addresses.street2 = %(street2)s AND addresses.city = %(city)s AND addresses.state = %(state)s AND addresses.zipcode = %(zipcode)s ORDER BY users.last_name ASC'
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if results:
            return results[0]
        else:
            return results

    # update an address
    @classmethod
    def edit_address(cls, data):
        query = "UPDATE addresses SET street1=%(street1)s, street2=%(street2)s, city=%(city)s, state=%(state)s, zipcode=%(zipcode)s, country=%(country)s, updated_at=NOW() WHERE addresses.id=%(id)s;"
        return connectToMySQL(SCHEMA).query_db(query, data)

    # assigns an existing address to a user
    @classmethod
    def assign_address(cls, data):
        query = "UPDATE users SET address_id = %(id)s;"
        return connectToMySQL(SCHEMA).query_db(query, data)

    # deletes an address
    @classmethod
    def remove_address(cls, data):
        query = "DELETE FROM addresses WHERE id = %(address_id)s;"
        return connectToMySQL(SCHEMA).query_db(query, data)