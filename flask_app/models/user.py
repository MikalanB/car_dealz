from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import car

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
    
    @classmethod
    def add_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"
        result = connectToMySQL("cars_schema").query_db(query,data)
        return result
    
    @classmethod
    def find_email (cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('cars_schema').query_db(query,data)
        if (len(result) < 1):
            return False
        return cls(result[0])
    
    @classmethod
    def find_id (cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('cars_schema').query_db(query,data)
        return cls(result[0])

    @staticmethod
    #validate user
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 alphabetic characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 alphabetic characters")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("This is an invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Passwords do no match! Please re-enter password.")
            is_valid = False
        return is_valid