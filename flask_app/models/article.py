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
        query = '''
            INSERT INTO articles 
            (title, description, content, url, image, published_at, source_name, source_url, created_at, updated_at) 
            VALUES 
            (%(title)s,%(description)s,%(content)s,%(url)s,%(image)s,%(published_at)s,%(source_name)s,%(source_url)s,NOW(),NOW());
        '''
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_all_articles(cls):
        query = 'SELECT * FROM articles;'
        results = connectToMySQL(cls.db).query_db(query)
        articles = []
        for article in results:
            articles.append(cls(article))
        return articles


    @classmethod
    def get_one_article(cls,article_id):
        query = "SELECT * from articles WHERE id = %(id)s;"
        data = {'id': article_id}
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])