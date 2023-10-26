from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.article import Article
from flask_app.models.artist import Artist
from flask_app.models.article_like import ArticleLike



@app.route('/dashboard')
def homepage():
    if 'userid' not in session:
        return redirect('/login')

    articles = Article.get_all_articles()
    artists = Artist.get_all_artists()
    featured = Article.get_featured_articles()
    # response = requests.get(f"https://gnews.io/api/v4/top-headlines?category=entertainment&lang=en&country=us&max=10&apikey={os.environ.get('GNEWS_API_KEY')}")
    
    # if response.status_code == 200:
    #     articles = response.json().get('articles')

    #     for article in articles:
    #         published_at = article.get('publishedAt')
    #         if published_at:
    #             article['publishedAt'] = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")

    # else:
    #     articles = []
    
    return render_template('dashboard.html',articles=articles, artists=artists,featured=featured) # if user logged in send to dashboard



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

    return render_template('one_article_page.html', article=article)

@app.route('/articles/like/<int:article_id>',methods=['POST'])
def like_article(article_id):
    if 'userid' not in session:
        return redirect('/login')
    
    print(session['userid'])
    user_id = session['userid']

    ArticleLike.add(user_id, article_id)

    return redirect('/articles/' + str(article_id))
