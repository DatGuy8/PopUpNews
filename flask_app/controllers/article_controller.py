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

    articles = Article.get_not_featured_articles()
    artists = Artist.get_all_artists()
    featured = Article.get_featured_articles()

    user = User.get_user_by_id(session['userid'])

    # if user logged in send to dashboard
    return render_template('dashboard.html', articles=articles, artists=artists, featured=featured, user=user)


@app.route('/articles', defaults={'page': 1})
@app.route('/articles/page/<int:page>')
def all_articles(page):
    per_page = 10
    articles = Article.get_paginated_articles(page, per_page)
    featured = Article.get_featured_articles()
    total_articles = Article.get_articles_count()
    total_pages = total_articles // per_page
    if total_articles % per_page != 0:
        total_pages += 1
    
    has_prev = page > 1
    has_next = page < total_pages
    prev_page = page - 1 if has_prev else None
    next_page = page + 1 if has_next else None
    return render_template('articles_page.html', featured=featured, articles=articles, total_pages=total_pages, has_prev=has_prev, has_next=has_next, prev_page=prev_page, next_page=next_page,current_page=page)


@app.route('/articles/<int:article_id>')
def one_article_page(article_id):
    if 'userid' not in session:
        return redirect('/login')

    article = Article.get_one_article(article_id)

    comments = Comment.get_comments_from_article_id(article_id)

    return render_template('one_article_page.html', article=article, comments=comments)


@app.route('/articles/like/<int:article_id>', methods=['POST'])
def like_article(article_id):
    if 'userid' not in session:
        return redirect('/login')

    user_id = session['userid']

    ArticleLike.add(user_id, article_id)

    return redirect('/articles/' + str(article_id))


@app.route('/articles/unlike/<int:article_id>', methods=['POST'])
def unlike_article(article_id):
    if 'userid' not in session:
        return redirect('/login')

    user_id = session['userid']
    ArticleLike.remove_like(user_id, article_id)

    return redirect('/articles/' + str(article_id))


@app.route('/articles/dashboard/like', methods=['POST'])
def testing():
    if 'userid' not in session:
        return redirect('/login')

    article_id = request.form['article_id']
    user_id = session['userid']
    liked = request.form['liked']

    if liked == 'TRUE':
        ArticleLike.remove_like(user_id, article_id)
        print('here')
    else:
        ArticleLike.add(user_id, article_id)
        print('there')

    likes_count = ArticleLike.like_count_by_article_id(article_id)

    return jsonify({'likes_count': likes_count})
