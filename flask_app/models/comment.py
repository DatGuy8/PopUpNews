from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    db = 'music_news_db'
    def __init__(self,data):
        self.id = data['id']
        self.article_id = data['article_id']
        self.user_id = data['user_id']
        self.parent_comment_id = data['parent_comment_id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.likes_count = data['likes_count']