from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.artist import Artist
from flask_app.models.user import User
from datetime import datetime
from flask_app.models.favorite_artist import FavoriteArtist
import os

import requests

@app.route('/artists',defaults={'page':1})
@app.route('/artist/search',defaults={'page':1})
@app.route('/artists/page/<int:page>')
def all_artists_page(page):
    per_page = 10
    artists = Artist.get_paginated_artists(page,per_page)
    total_artists = Artist.get_artists_count()
    total_pages = total_artists // per_page
    if total_artists % per_page != 0:
        total_pages += 1
    
    has_prev = page > 1
    has_next = page < total_pages
    prev_page = page - 1 if has_prev else None
    next_page = page + 1 if has_next else None
    searchedArtist = {}
    searchPage=False

    if(request.args.get('artist_name')):
        searchPage=True
        artist_name = request.args.get('artist_name')
        print(artist_name)

        url = "https://theaudiodb.p.rapidapi.com/search.php"

        querystring = {"s": artist_name}

        headers = {
            "X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
            "X-RapidAPI-Host": "theaudiodb.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        searchedArtist = {}

        if response.status_code == 200:
            returnArtist = response.json().get('artists')
            if returnArtist is not None and len(returnArtist) > 0:
                searchedArtist = returnArtist[0]
            else:
                searchedArtist = {}

    return render_template('all_artists_page.html', searchedArtist=searchedArtist, artists=artists, searchPage=searchPage, total_pages=total_pages, has_prev=has_prev, has_next=has_next, prev_page=prev_page, next_page=next_page,current_page=page)


@app.route('/artist/add', methods=['POST'])
def add_artist_to_db():
    artist = Artist.add_artist(request.form)
    print('got artist', artist)
    return redirect('/artists')


@app.route('/artists/<int:artist_id>')
def one_artist_page(artist_id):

    user_id = session['userid']
    user = User.get_user_by_id(user_id)
    artist = Artist.get_one_artist(artist_id)

    response = requests.get(
        f"https://gnews.io/api/v4/top-headlines?category=entertainment&lang=en&&q={artist.name}&country=us&max=20&apikey={os.environ.get('GNEWS_API_KEY')}&expand=content")
    if response.status_code == 200:
        articles = response.json().get('articles')

        for article in articles:
            published_at = article.get('publishedAt')
            if published_at:
                article['publishedAt'] = datetime.strptime(
                    published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
    else:
        articles = []
    print(response)

    return render_template('single_artist_page.html', artist=artist, articles=articles, user=user)


@app.route('/artists/favorite/<int:artist_id>', methods=['POST'])
def add_favourite_artist(artist_id):
    if 'userid' not in session:
        return redirect('/login')

    user_id = session['userid']

    FavoriteArtist.add(user_id, artist_id)

    print('added artists to favorites')
    return redirect('/artists/' + str(artist_id))
