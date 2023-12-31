from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class FavoriteArtist:
    db = 'music_news_db'
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.artist_id = data['artist_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.artists = []

    @classmethod
    def add(cls, user_id, artist_id):
        query = '''
            INSERT INTO favorite_artists (user_id, artist_id,created_at,updated_at)
            VALUES ( %(user_id)s, %(artist_id)s, NOW(),NOW());
        ''' 
        data = {'user_id':user_id, 'artist_id': artist_id}
        return connectToMySQL(cls.db).query_db(query,data)
    
    # @classmethod
    # def get_one_users_fav(cls, user_id):
    #     query = '''
    #         SELECT * FROM favorite_artists left join artists On artists.id = artist_id where user_id = %(id)s;
    #     '''
    #     data = {'id': user_id}
        
    #     artists = []
    #     results = connectToMySQL(cls.db).query_db(query, data)
    #     for artist in results:
