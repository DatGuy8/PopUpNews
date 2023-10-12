from flask_app import app
from flask import render_template, redirect, request, session, flash,jsonify
from datetime import datetime
from flask_app.models.article import Article
import os
import requests

@app.route('/admin/users')
def admin_users():
    return render_template('admin_users.html')

@app.route('/admin/articles')
def admin_articles():

    response = requests.get(f"https://gnews.io/api/v4/top-headlines?category=entertainment&lang=en&country=us&max=20&apikey={os.environ.get('GNEWS_API_KEY')}&expand=content")
    
    if response.status_code == 200:
        articles = response.json().get('articles')

        for article in articles:
            published_at = article.get('publishedAt')
            if published_at:
                article['publishedAt'] = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")

    else:
        articles = []


    print(articles)
    return render_template('admin_articles.html', articles=articles)

@app.route('/admin/artists')
def admin_artists():
    return render_template('admin_artists.html')


@app.route('/admin/articles/add', methods=['POST'])
def add_article_to_db():
    

    article = Article.add_article(request.form)
    return redirect('/dashboard')