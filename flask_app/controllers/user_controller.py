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