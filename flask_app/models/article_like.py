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
    
    @classmethod
    def remove_like(cls,user_id,article_id):
        query = '''
            DELETE FROM article_likes WHERE user_id = %(user_id)s AND article_id = %(article_id)s;
        '''
        data = {
            'user_id':user_id,
            'article_id': article_id
            }
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_by_article_id(cls,article_id):
        query = '''
            DELETE FROM article_likes WHERE article_id = %(id)s;
        '''
        data = {'id' : article_id}
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_users_id_by_article_id(cls,article_id):
        query = '''
            SELECT user_id FROM article_likes WHERE article_id = %(id)s;
        '''
        data = {'id': article_id}
        results = connectToMySQL(cls.db).query_db(query,data)
        users_ids = []
        for row in results:
            users_ids.append(row['user_id'])

        return users_ids

    @classmethod
    def like_count_by_article_id(cls,article_id):
        query = '''
            SELECT COUNT(*) AS like_count
            FROM article_likes
            WHERE article_id = %(id)s;
        '''
        data = {"id" : article_id}
        result = connectToMySQL(cls.db).query_db(query,data)

        return result[0]['like_count']
