import datetime
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import os
import base64
import app as main

comment_handling = Blueprint('comment_handling', __name__, template_folder='templates')

@comment_handling.route('/comments/<int:picture_id>', methods=['GET'])
def comments(picture_id, msg = None):
    cursor = main.conn.cursor()
    cursor.execute("SELECT text, first_name, date, Comments.user_id FROM Comments INNER JOIN Users ON Comments.user_id = Users.user_id WHERE picture_id = {0}".format(picture_id))
    comments = cursor.fetchall()
    return render_template('comments.html', comments=comments, picture_id = picture_id, message = msg)

@comment_handling.route('/comments/<int:picture_id>', methods=['POST'])
def user_commented(picture_id):
    cursor = main.conn.cursor()
    try:
        uid = main.getUserIdFromEmail(flask_login.current_user.id)
    except:
        uid = -1
    date = datetime.date.today()
    text = request.form.get("comment")
    try:
        cursor.execute('''INSERT INTO Comments (user_id, date, picture_id, text) VALUES (%s, %s, %s , %s )''', (uid, date, picture_id, text))
        main.conn.commit()
        return comments(picture_id, "Comment added")
    except:
        return comments(picture_id, "You can not comment on your own post")

@comment_handling.route('/comment_search', methods=['GET'])
def comment_search():
    return render_template('comment_search.html')

@comment_handling.route('/comment_search', methods=['POST'])
def grab_comments():
    text = str(request.form.get("comment"))
    cursor = main.conn.cursor()
    #[(user_id, date, text, imgdata)]
    cursor.execute("SELECT Comments.user_id, Comments.date, Comments.text, Pictures.imgdata FROM Comments INNER JOIN Pictures ON Comments.picture_id = Pictures.picture_id WHERE text = '{0}'".format(text))
    comments = cursor.fetchall()
    return render_template('comment_search.html', comments = comments, base64 = base64)
