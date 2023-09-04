from flask_app import app
from flask import render_template, redirect, request, session, flash

@app.route('/')
def home():
    if 'userid' in session:
        return redirect('/dashboard')    # if user logged in send to dashboard

    return render_template('login_page.html')