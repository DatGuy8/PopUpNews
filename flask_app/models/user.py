from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'music_news_db'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.admin = data['admin']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_user(cls,data):
        query = 'INSERT INTO users (username,first_name, last_name, email, password, created_at, updated_at) VALUES (%(username)s,%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s ;'
        result = connectToMySQL(cls.db).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users


    @staticmethod
    def validate_form(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('music_news_db').query_db(query, data)
        
        if len(data['username']) < 3:
            flash('Username must have at least 3 characters', 'username')
            is_valid = False

        if len(results) >= 1:
            flash('Email Already Taken!', 'registration')
            is_valid = False
        
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", 'registration')
            is_valid = False
        
        if not data['first_name'].isalpha() or not data['last_name'].isalpha():
            flash('Names must not have numbers in it', 'registration')
            is_valid = False
        
        if len(data['first_name']) < 3:
            flash('First Name must be longer than 2 characters', 'registration')
            is_valid = False
        
        if len(data['last_name']) < 2:
            flash("Last name must have at least 2 characters", 'registration')
            is_valid = False
        
        if len(data['password']) < 8:
            flash('PASSWORD NEEDS TO BE AT LEAST 8 CHARACTERS', 'registration')
            is_valid = False
        
        if data['password'] != data['conpassword']:
            flash('PASSWORDS DO NOT MATCH!', 'registration')
            is_valid = False
        # if not PASS_REGEX.match(data['password']):
        #     flash('MUST CONTAIN ONE UPPERCASE LETTER AND A NUMBER IN PASSWORD also no special characters', 'registration')
            # is_valid = False
        return is_valid