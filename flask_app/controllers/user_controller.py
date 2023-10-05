from flask_app import app
from flask import render_template, redirect, request, session, flash

@app.route('/')
def home():
    # if 'userid' in session:
    #     return redirect('/dashboard')    # if user logged in send to dashboard

    return redirect('/dashboard')


@app.route('/dashboard')
def homepage():
    return render_template('dashboard.html')

@app.route('/login')
def login_page():
    return render_template('login_page.html')


@app.route('/articles')
def all_articles():
    return render_template('articles_page.html')

@app.route('/articles/<int:article_id>')
def one_article_page(article_id):
    return render_template('one_article_page.html')


@app.route('/user/feed')
def user_feed():
    return render_template('user_feed.html')

@app.route('/users/<int:user_id>')
def profile_page(user_id):
    return render_template('profile_page.html')

@app.route('/artists')
def all_artists_page():
    return render_template('all_artists_page.html')


@app.route('/artists/<int:artist_id>')
def one_artist_page(artist_id):
    return render_template('single_artist_page.html')


@app.route('/admin/users')
def admin_users():
    return render_template('admin_users.html')

@app.route('/admin/articles')
def admin_articles():
    return render_template('admin_articles.html')

@app.route('/admin/artists')
def admin_artists():
    return render_template('admin_artists.html')