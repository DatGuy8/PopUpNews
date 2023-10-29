from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.comment import Comment


@app.route('/articles/newcomment/<int:article_id>',methods=['POST'])
def add_comment(article_id):
    if 'userid' not in session:
        return redirect('/login')
    
    print('commentroute')

    Comment.add_comment(article_id,session['userid'],request.form['parent_comment_id'],request.form['comment'])
    
    print('commentrouteafter')
    return redirect('/articles/' + str(article_id))
