from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
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
@app.route('/registeruser', methods=['POST'])
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

    if not register_user:
        flash('Invalid Email/Password', 'login')
        return redirect('/login')

    if not bcrypt.check_password_hash(registered_user.password, request.form['password']):   # Checks password correct
        flash('Invalid Email/Password', 'login')
        return redirect('/login') 


    session['userid'] = registered_user.id
    print('logged in' , register_user)
    return redirect('/dashboard')



@app.route('/logout')       #Clears session and send back to login page
def logout():

    session.clear()
    return redirect('/')













@app.route('/dashboard')
def homepage():
    if 'userid' in session:
        return render_template('dashboard.html')    # if user logged in send to dashboard

    return redirect('/login')



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