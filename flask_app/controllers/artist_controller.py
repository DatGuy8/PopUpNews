from flask_app import app
from flask import render_template, redirect, request, session, flash,jsonify
from flask_app.models.artist import Artist
from datetime import datetime
import os

import requests


@app.route('/artist/search')
def search_artist():
    artist_name = request.args.get('artist_name')
    print(artist_name)

    url = "https://theaudiodb.p.rapidapi.com/search.php"

    querystring = {"s": artist_name}

    headers = {
        "X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
        "X-RapidAPI-Host": "theaudiodb.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

    if response.status_code == 200:
        returnArtist = response.json().get('artists')

        artist = returnArtist[0]
    else:
        artist = {}
    return render_template('all_artists_page.html', artist=artist)

@app.route('/artists')
def all_artists_page():
    artists = Artist.get_all_artists()
    searchedArtist = {}
    return render_template('all_artists_page.html', searchedArtist=searchedArtist, artists=artists)


@app.route('/artist/add', methods=['POST'])
def add_artist_to_db():
    artist = Artist.add_artist(request.form)
    print('got artist', artist)
    return redirect('/artists')


@app.route('/artists/<int:artist_id>')
def one_artist_page(artist_id):
    artist = Artist.get_one_artist(artist_id)

    response = requests.get(f"https://gnews.io/api/v4/top-headlines?category=entertainment&lang=en&&q={artist.name}&country=us&max=20&apikey={os.environ.get('GNEWS_API_KEY')}&expand=content")
    if response.status_code == 200:
        articles = response.json().get('articles')

        for article in articles:
            published_at = article.get('publishedAt')
            if published_at:
                article['publishedAt'] = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
    else:
        articles = []
    print(response)
    
    return render_template('single_artist_page.html', artist=artist, articles=articles)