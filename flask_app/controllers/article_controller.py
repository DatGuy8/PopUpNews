from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.article import Article
from flask_app.models.artist import Artist
from flask_app.models.article_like import ArticleLike
from flask_app.models.comment import Comment
from flask_app.models.user import User



@app.route('/dashboard')
def homepage():
    if 'userid' not in session:
        return redirect('/login')

    articles = Article.get_all_articles()
    artists = Artist.get_all_artists()
    featured = Article.get_featured_articles()
    user = User.get_user_by_id(session['userid'])
    
    return render_template('dashboard.html',articles=articles, artists=artists,featured=featured,user=user) # if user logged in send to dashboard



@app.route('/articles')
def all_articles():
    articles = Article.get_all_articles()
    featured = Article.get_featured_articles()
    return render_template('articles_page.html',featured=featured,articles=articles)


@app.route('/articles/<int:article_id>')
def one_article_page(article_id):
    if 'userid' not in session:
        return redirect('/login')

    article = Article.get_one_article(article_id)

    comments = Comment.get_comments_from_article_id(article_id)

    return render_template('one_article_page.html', article=article,comments=comments)

@app.route('/articles/like/<int:article_id>',methods=['POST'])
def like_article(article_id):
    if 'userid' not in session:
        return redirect('/login')
    
    
    user_id = session['userid']

    ArticleLike.add(user_id, article_id)

    return redirect('/articles/' + str(article_id))

@app.route('/articles/unlike/<int:article_id>',methods=['POST'])
def unlike_article(article_id):
    if 'userid' not in session:
        return redirect('/login')
    
    user_id = session['userid']
    ArticleLike.remove_like(user_id, article_id)

    return redirect('/articles/' + str(article_id))

@app.route('/testing',methods=['POST'])
def testing():
    if 'userid' not in session:
        return redirect('/login')
    
    
    user_id = session['userid']
    article_id = request.form['article_id']
    print(ArticleLike.like_count_by_article_id(article_id))
    ArticleLike.add(user_id, article_id)
    likes_count = ArticleLike.like_count_by_article_id(article_id)
    print("after", likes_count)
    # write code to save it to our database . . .
    return jsonify({'likes_count': likes_count})
    