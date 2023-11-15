from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import article_like
from flask_app.models import comment


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
        self.priority = data['priority']
        self.featured = data['featured']
        self.likes = 0
        self.user_likes = []
        self.comment_count = 0


    @classmethod
    def add_article(cls,data):
        query = '''
            INSERT INTO articles 
            (title, description, content, url, image, published_at, source_name, source_url,priority, created_at, updated_at) 
            VALUES 
            (%(title)s,%(description)s,%(content)s,%(url)s,%(image)s,%(published_at)s,%(source_name)s,%(source_url)s,%(priority)s,NOW(),NOW());
        '''
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_all_articles(cls):
        query = '''
            SELECT articles.*, COUNT(DISTINCT article_likes.user_id) AS likes_count, COUNT(DISTINCT comments.id) AS comment_count
            FROM articles
            LEFT JOIN article_likes ON article_likes.article_id = articles.id
            LEFT JOIN comments ON comments.article_id = articles.id
            GROUP BY articles.id;
        '''
        results = connectToMySQL(cls.db).query_db(query)
        articles = []
        for article in results:
            one_article = cls(article)
            one_article.likes = article['likes_count']
            one_article.comment_count = article['comment_count']
            one_article.user_likes = article_like.ArticleLike.get_users_id_by_article_id(article['id'])
            articles.append(one_article)
        return articles

    
    @classmethod
    def get_featured_articles(cls):
        query = '''
            SELECT articles.*, COUNT(DISTINCT article_likes.user_id) as likes_count, COUNT(DISTINCT comments.id) AS comment_count
            FROM articles
            LEFT JOIN article_likes ON article_likes.article_id = articles.id
            LEFT JOIN comments ON comments.article_id = articles.id
            WHERE articles.featured = 1
            GROUP BY articles.id
            ORDER BY articles.priority ASC;
        '''
        results = connectToMySQL(cls.db).query_db(query)
        featured = []
        for article in results:
            one_article = cls(article)
            one_article.likes = article['likes_count']
            one_article.user_likes = article_like.ArticleLike.get_users_id_by_article_id(article['id'])
            one_article.comment_count = article['comment_count']
            featured.append(one_article)
        return featured

    @classmethod
    def get_not_featured_articles(cls):
        query = '''
            SELECT articles.*, COUNT(DISTINCT article_likes.user_id) as likes_count, COUNT(DISTINCT comments.id) AS comment_count
            FROM articles
            LEFT JOIN article_likes ON article_likes.article_id = articles.id
            LEFT JOIN comments ON comments.article_id = articles.id
            WHERE articles.featured = 0
            GROUP BY articles.id
            ORDER BY articles.updated_at DESC;
        '''
        results = connectToMySQL(cls.db).query_db(query)
        articles = []
        for article in results:
            one_article = cls(article)
            one_article.likes = article['likes_count']
            one_article.user_likes = article_like.ArticleLike.get_users_id_by_article_id(article['id'])
            one_article.comment_count = article['comment_count']
            articles.append(one_article)
        return articles

    @classmethod
    def get_one_article(cls,article_id):
        query = """
            SELECT articles.*, COUNT(DISTINCT comments.id) AS comment_count
            FROM articles 
            LEFT JOIN comments ON comments.article_id = articles.id
            WHERE articles.id = %(id)s;
        """
        data = {'id': article_id}
        result = connectToMySQL(cls.db).query_db(query,data)
        
        one_article = result[0]
        
        article = cls(one_article)

        article.user_likes = article_like.ArticleLike.get_users_id_by_article_id(article_id)
        article.likes = len(article.user_likes)
        article.comment_count = result[0]['comment_count']

        return article

    @classmethod
    def change_featured(cls,article_id, featured):
        query = '''
            UPDATE articles SET featured = %(featured)s, updated_at = NOW() WHERE id = %(id)s;
        '''
        data = {'id' : article_id, 'featured': '0' if featured else '1' }
        
        
        return connectToMySQL(cls.db).query_db(query,data)
    

    @classmethod
    def delete(cls,article_id):
        query = '''
            DELETE FROM articles where id = %(id)s;
        '''
        # delete the likes
        article_like.ArticleLike.delete_by_article_id(article_id)
        # delete comments
        comment.Comment.delete_by_id(article_id)
        data = {'id': article_id}
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_articles_by_user_id(cls, user_id):
        query = '''
            SELECT *
            FROM articles
            JOIN article_likes ON articles.id = article_likes.article_id
            WHERE article_likes.user_id = %(id)s;
        '''

        data = {'id': user_id}
        results = connectToMySQL(cls.db).query_db(query,data)
        articles = []
        
        for article in results:
            articles.append(cls(article))
        return articles
    
    @classmethod
    def update_priority(cls,article_id, priority_int):
        query = '''
            UPDATE articles SET priority = %(priority_int)s
            WHERE id = %(article_id)s;
        '''

        data = {
            'article_id': article_id,
            'priority_int': priority_int
        }

        return connectToMySQL(cls.db).query_db(query,data)