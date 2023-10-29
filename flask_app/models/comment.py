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
        self.username = data['username']
        
        

    
    @classmethod
    def add_comment(cls,article_id, user_id, parent_comment_id, comment):
        query = '''
            INSERT INTO comments (article_id, user_id, comment, parent_comment_id, created_at, updated_at)
            VALUES (%(article_id)s,%(user_id)s,%(comment)s,%(parent_comment_id)s,NOW(),NOW());
        '''
        data = {
            'article_id' : article_id,
            'user_id' : user_id,
            'parent_comment_id': parent_comment_id,
            'comment': comment
        }

        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_comments_from_article_id(cls,article_id):
        query = '''
            SELECT comments.*, users.username
            FROM comments
            LEFT JOIN users ON comments.user_id = users.id
            WHERE comments.article_id = %(article_id)s
            ORDER BY comments.created_at;
        '''
        data = {'article_id': article_id}
        results = connectToMySQL(cls.db).query_db(query, data)

        comments = []
        for result in results:
            
            comment_data = {
                'id': result['id'],
                'article_id': result['article_id'],
                'user_id': result['user_id'],
                'parent_comment_id': result['parent_comment_id'],
                'comment': result['comment'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'username': result['username']
            }
            comments.append(cls(comment_data))

        top_comments = []
        replies = {}
        for one_comment in comments:
            if one_comment.parent_comment_id is None:
                top_comments.append(one_comment)
            else:
                parent_id = one_comment.parent_comment_id
                if parent_id not in replies:
                    replies[parent_id] = [one_comment]
                else:
                    replies[parent_id].append(one_comment)

        for comment in top_comments:
            if comment.id in replies:
                comment.replies = replies[comment.id]


        return top_comments