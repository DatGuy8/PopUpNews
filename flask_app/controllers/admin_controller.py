from flask_app import app
from flask import render_template, redirect, request, session, flash,jsonify
from datetime import datetime
from flask_app.models.article import Article
import os
import requests
import re

@app.route('/admin/users')
def admin_users():
    return render_template('admin_users.html')

@app.route('/admin/articles')
def admin_articles():

    response = requests.get(f"https://gnews.io/api/v4/search?q=music&lang=en&country=us&max=50&apikey={os.environ.get('GNEWS_API_KEY')}&expand=content")
    
    if response.status_code == 200:
        articles = response.json().get('articles')

        for article in articles:
            published_at = article.get('publishedAt')
            if published_at:
                article['publishedAt'] = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
    else:
        articles = []

    return render_template('admin_articles.html', articles=articles)

@app.route('/admin/artists')
def admin_artists():
    return render_template('admin_artists.html')


@app.route('/admin/articles/add', methods=['POST'])
def add_article_to_db():
    article = Article.add_article(request.form)
    return redirect('/dashboard')

@app.route('/admin/savedarticles')
def admin_saved_articles():
    articles = Article.get_all_articles()

    return render_template('admin_db_articles.html',articles=articles)

@app.route('/admin/articles/feature/<int:article_id>',methods=['POST'])
def feature_article(article_id):
    featured = request.form['featured'] == '1'
    Article.change_featured(article_id,featured)

    return redirect('/admin/savedarticles')

@app.route('/admin/articles/delete/<int:article_id>',methods=['POST'])
def delete_article(article_id):

    Article.delete(article_id)
    return redirect('/admin/savedarticles')