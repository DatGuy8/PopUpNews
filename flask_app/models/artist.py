from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Artist:
    db = 'music_news_db'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.picture = data['picture']
        self.bio = data['bio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def add_artist(cls,data):
        pass