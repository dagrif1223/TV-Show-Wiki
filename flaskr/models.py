from flask_login import LoginManager, UserMixin
from flask import Flask
from itsdangerous import URLSafeTimedSerializer

"""
User class which gets username and returns unique id for the user
Includes method like is_authenticated, logout user, get_name which are used in pages
"""


class User(UserMixin):

    def __init__(self, username, active=True):
        self.username = username
        self.active = active

    def get_id(self):
        current_user = self.username
        return current_user

    def __str__(self):
        return "%s" % (self.username)

    def is_active(self):
        return self.active

    def __repr__(self):
        return f"User('{self.username}')"

    def is_authenticated(self):
        return True

    def logout_user(self):
        return False

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.username

    def set_last_name(self,last_name):
        self.last_name = last_name
    
    def get_last_name(self,last_name):
        return self.last_name
    
    def set_email(self,email):
        self.email = email
    
    def get_email(self,email):
        return self.email

