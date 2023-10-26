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
        query = '''
            INSERT INTO artists
            (name, picture, bio, created_at, updated_at) 
            VALUES 
            (%(name)s,%(picture)s,%(bio)s,NOW(),NOW());
        '''
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_one_artist(cls,artist_id):
        query = '''
            SELECT * FROM artists WHERE id = %(id)s;
        '''
        data = {'id': artist_id}
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all_artists(cls):
        query = '''
            SELECT * FROM artists;
        '''
        results = connectToMySQL(cls.db).query_db(query)
        artists = []
        for artist in results:
            artists.append(cls(artist))
        return artists
    

