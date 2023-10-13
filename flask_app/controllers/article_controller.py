from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.article import Article


@app.route('/articles/<int:article_id>')
def one_article_page(article_id):

    article = Article.get_one_article(article_id)

    return render_template('one_article_page.html', article=article)