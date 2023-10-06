from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class CommentLike:
    db = 'music_news_db'
    def __init__(self,data):
        self.id = data['id']
        self.comment_id = data['comment_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']