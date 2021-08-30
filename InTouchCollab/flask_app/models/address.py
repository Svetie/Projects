from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
# from flask_app.models.group import Group
import re


class Address:
    def __init__(self, data):
        self.id = data['id']
        self.street1 = data['street1']
        self.street2 = data['street2']
        self.city  = data['city']
        self.state  = data['state']
        self.zipcode  = data['zipcode']
        self.country = data['country']

        self.users = []