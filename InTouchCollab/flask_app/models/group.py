from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.address import Address
import re

SCHEMA = 'users_groups_schema'
NAME_REGEX  = re.compile(r'^[a-zA-Z\s]+$')
# DESC_REGEX  = re.compile(r'^[a-zA-Z\s]+$')
# DESC_REGEX = re.compile('^(?=.*[A-Z0-9])[\w.,!"'\/$ ]+$')

class Group:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description  = data['description']
        self.updated_at = data['updated_at']

        self.users = []

    @staticmethod
    def validate(group):
        name_valid = False
        desc_valid = False

        ############--Group name
        length = len(group['name'])
        if ( length >= 3 and length <= 45 ):
            if NAME_REGEX.match(group['name']):
                name_valid = True
            else:
                flash('Name must be alphanumeric.', 'warning')
                print('Name must be alphanumeric.', 'warning')
        else:
            flash("Name must be at least 3 characters and no more than 45 characters long.", 'warning')
            print("Name must be at least 3 characters and no more than 45 characters long.", 'warning')

        ##############--Description
        length = len(group['description'])
        if ( length >= 3 and length <= 16 ):
            if DESC_REGEX.match(group['description']):
                desc_valid = True
                print('Description is valid')
            else:
                flash('Description must be alphanumeric only.', 'warning')
                print('Description must be alphanumeric only.', 'warning')
        else:
            flash("First name must be at least 3 characters and no more than 16 characters long.", 'warning')
            print("First name must be at least 3 characters and no more than 16 characters long.", 'warning')

        print('combined valid states are:', name_valid and desc_valid)
        return (name_valid and desc_valid)

    # get all groups
    @classmethod
    def get_all_groups(cls):
        query = "SELECT * FROM ugroups ORDER BY name ASC;"
        results = connectToMySQL(SCHEMA).query_db(query)
        groups = []
        for group in results:
            groups.append(cls(group))
        return groups

    # get one group by ID
    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM ugroups WHERE id = %(id)s'
        results = connectToMySQL(SCHEMA).query_db(query, data)

        if results:
            return cls( results[0] )
        else:
            return results

    #get one group by a name
    @classmethod
    def get_group_by_name(cls, data):
        query = 'SELECT * FROM ugroups WHERE name = %(name)s'
        results = connectToMySQL(SCHEMA).query_db(query, data)

        if results:
            return results[0]
        else:
            return results

    #get all users that belong to a group
    @classmethod
    def get_users_in_group(cls, data):
        query = "SELECT * FROM ugroups LEFT JOIN user_group ON ugroups.id = user_group.ugroup_id LEFT JOIN users ON user_group.user_id = users.id LEFT JOIN addresses ON users.address_id = addresses.id WHERE ugroups.id = %(id)s;"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if not results:
            return False
        else:
            group = cls( results[0] ) 

            for line in results:
                address_data = {
                    "id" : line['addresses.id'],
                    "street1" : line['street1'],
                    "street2" : line['street2'],
                    "city"  : line['city'],
                    "state"  : line['state'],
                    "zipcode"  : line['zipcode'],
                    "country" : line['country'],
                    "created_at" : line['addresses.created_at'],
                    "updated_at" : line['addresses.updated_at']
                }
                address = Address(address_data)
                print('address==================', address_data['id'])
                print('address==================', address.city)
                user_data = {
                    "id" : line['users.id'],
                    "first_name" : line['first_name'],
                    "last_name"  : line['last_name'],
                    "email"      : line['email'],
                    "password"   : line['password'],
                    "phone"      : line['phone'],
                    "phone_alt"  : line['phone_alt'],
                    "created_at" : line['created_at'],
                    "updated_at" : line['updated_at'],
                    "address_id" : address.id,
                    # "address" : address
                }
                user_new = User(user_data)
                user_new.address = address
                group.users.append( user_new )
            return group

    #add one group
    @classmethod
    def add_group(cls, data):
        query = "INSERT INTO ugroups ( name, description, created_at, updated_at ) VALUES ( %(name)s, %(description)s, NOW() , NOW() );"
        return connectToMySQL(SCHEMA).query_db(query, data)

    # update one group
    @classmethod
    def edit(cls, data):
        query = "UPDATE ugroups SET name = %(name)s, description = %(description)s, updated_at=NOW() WHERE id =%(id)s"
        return connectToMySQL(SCHEMA).query_db(query, data)

    # delete one group
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM ugroups WHERE id = %(id)s;"
        return connectToMySQL(SCHEMA).query_db(query, data)

    # get all users in one group
    @classmethod
    def get_users(cls, data):
        query = f"SELECT Users.* FROM ugroups INNER JOIN user_group ON ugroups.id = user_group.group_id INNER JOIN users ON user_group.user_id = users.id WHERE ugroups.id = %(group_id)s"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        entries = []
        for item in results:
            entries.append(cls(item))
        return entries

    # get all groups that a user belongs to
    @classmethod
    def getby_user(cls, data):
        query = f"SELECT ugroups.* FROM ugroups INNER JOIN user_group ON ugroups.id = user_group.group_id INNER JOIN users ON user_group.user_id = users.id WHERE users.id = %(user_id)s"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        entries = []
        for item in results:
            entries.append(cls(item))
        return entries

    # add a user to a group
    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO user_group (user_id, group_id) VALUES (%(user_id)s, %(group_id)s);"
        return connectToMySQL(SCHEMA).query_db(query, data)

    # remove a user from a group
    @classmethod
    def remove_user(cls, data):
        query = "DELETE FROM user_group WHERE group_id = %(group_id)s AND user_id = %(user_id)s;"
        return connectToMySQL(SCHEMA).query_db(query, data)

    # check if a group already exists by a name
    @classmethod
    def check_exists(cls, data):
        query = "SELECT id FROM ugroups WHERE ( name = %(name)s )"
        results = connectToMySQL(SCHEMA).query_db(query, data)
        if results:
            return results[0]
        else:
            return results