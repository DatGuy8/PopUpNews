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
    def get_artists_count(cls):
        query = 'SELECT COUNT(*) AS total_artists FROM artists;'
        results = connectToMySQL(cls.db).query_db(query)
        return results[0]['total_artists']

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
    
    @classmethod
    def get_paginated_artists(cls,page=1,per_page=10):
        offset = (page-1) * per_page
        query = '''
            SELECT * FROM artists
            ORDER BY name ASC
            LIMIT %(per_page)s OFFSET %(page)s;
        '''
        data = {
            'per_page' : per_page,
            'page': offset
        }
        results = connectToMySQL(cls.db).query_db(query,data)
        artists = []
        for artist in results:
            artists.append(cls(artist))
        return artists
