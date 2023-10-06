from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Article:
    db = 'music_news_db'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.content = data['content']
        self.url = data['url']
        self.image = data['image']
        self.published_at = data['published_at']
        self.source_name = data['source_name']
        self.source_url = data['source_url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.likes_count = data['likes_count']
        self.featured = data['featured']


    @classmethod
    def add_article(cls,data):
        pass
