from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Painting:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # user object
        self.user = {}

    #*************************************
    #   Validate Painting
    #*************************************
    @staticmethod
    def validate_painting(data):
        is_valid = True

        # if fields are empty
        if not data['title']:
            flash("Title field is required")
            is_valid = False
        if not data['description']:
            flash("Description field is required")
            is_valid = False
        if not data['price']:
            flash("Price field is required")
            is_valid = False
        elif(float(data['price']) <= 0 ):
            flash('Price should be greater than 0')
            is_valid = False

        #length validation
        if(len(data['title']) <  2):
            flash('Title should be at least 2 letters long')
            is_valid = False
        if(len(data['description']) <  10):
            flash('Description should be at least 10 letters long')
            is_valid = False

        return is_valid

    #************************************************
    #   Save Painting
    #************************************************
    @classmethod
    def save_painting(cls, data):
        query = "INSERT INTO paintings (user_id, title, description, price, created_at, updated_at) VALUES (%(user_id)s, %(title)s, %(description)s, %(price)s, now(), now());"
        id = connectToMySQL("paintings_schema").query_db(query, data)

        return id

    ######################################
    #   Get one Painting info
    ######################################
    @classmethod
    def get_painting_info(cls, data):
        query = "SELECT * FROM paintings JOIN users ON users.id = user_id WHERE paintings.id = %(id)s;"
        results = connectToMySQL("paintings_schema").query_db(query, data)

        one_painting = cls( results[0] ) # creates an instance of a class we are inside of

        user_data = {
            "id" : results[0]['users.id'],
            "first_name" : results[0]['first_name'],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "created_at" : results[0]['users.created_at'],
            "updated_at" : results[0]['users.updated_at'],
        }

        one_painting.user = User(user_data)
        return one_painting

    #************************************************
    #   Get all paintings
    #************************************************
    @classmethod
    def get_all_paintings(csl):
        query = "SELECT * FROM paintings JOIN users ON users.id = user_id;"
        results = connectToMySQL("paintings_schema").query_db(query)

        paintings = []

        #loop through the results and parse data
        for row in results:
            one_painting = csl(row) #    create instance of car class

            user_data = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
            }

            one_painting.user = User(user_data)
            paintings.append(one_painting)
        return paintings

    ######################################
    #   Update Painting
    ######################################
    @classmethod
    def update_painting(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL("paintings_schema").query_db(query, data)
        return

    ######################################
    #   Delete Painting
    #####################################
    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        results = connectToMySQL("paintings_schema").query_db(query, data)
        return