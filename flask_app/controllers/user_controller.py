from flask_app import app
from flask import render_template, redirect, request, session, flash,jsonify
from flask_app.models.user import User
from flask_app.models.article import Article
from flask_bcrypt import Bcrypt
from datetime import datetime
import os

import requests
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    if 'userid' in session:
        return redirect('/dashboard')    # if user logged in send to dashboard

    return redirect('/login')

@app.route('/login')
def login_page():
    return render_template('login_page.html')

#=========REGISTER ROUTE==========
@app.route('/register', methods=['POST'])
def register_user():

    if not User.validate_form(request.form):
        return redirect('/login')

    pwhash = bcrypt.generate_password_hash(request.form['password'])      # creates hash password from the form
    data = {
        'username' : request.form['username'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pwhash
    }

    user = User.add_user(data)
    print('got user data:', user)
    return redirect('/dashboard')


@app.route('/login',methods=['POST'])
def login_user():

    data = {
        'email' : request.form['email']
    }
    registered_user = User.get_user_by_email(data)

    if not registered_user:
        flash('Invalid Email/Password', 'login')
        return redirect('/login')

    if not bcrypt.check_password_hash(registered_user.password, request.form['password']):   # Checks password correct
        flash('Invalid Email/Password', 'login')
        return redirect('/login') 


    session['userid'] = registered_user.id
    print('logged in' , registered_user.id)
    return redirect('/dashboard')



@app.route('/logout')       #Clears session and send back to login page
def logout():

    session.clear()
    return render_template('login_page.html')








@app.route('/user/feed')
def user_feed():
    return render_template('user_feed.html')

@app.route('/users/<int:user_id>')
def profile_page(user_id):
    if 'userid' not in session:
        return redirect('/login')


    user = User.get_user_by_id(user_id)
    
    return render_template('profile_page.html', user=user)



