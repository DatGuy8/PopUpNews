from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class ArticleLike:
    db = 'music_news_db'
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.article_id = data['article_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def add(cls,user_id,article_id):
        query = '''
            INSERT INTO article_likes (user_id, article_id,created_at,updated_at)
            VALUES ( %(user_id)s, %(article_id)s, NOW(),NOW());
        '''

        data = {'user_id':user_id, 'article_id': article_id}

        return connectToMySQL(cls.db).query_db(query,data)