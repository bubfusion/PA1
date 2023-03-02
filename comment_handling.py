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
def comments(picture_id):
    cursor = main.conn.cursor()
    cursor.execute("SELECT text, first_name, date FROM Comments INNER JOIN Users ON Comments.user_id = Users.user_id WHERE picture_id = {0}".format(picture_id))
    comments = cursor.fetchall()
    return render_template('comments.html', comments=comments, picture_id = picture_id)

@comment_handling.route('/comments/<int:picture_id>', methods=['POST'])
def user_commented(picture_id):
    cursor = main.conn.cursor()
    uid = main.getUserIdFromEmail(flask_login.current_user.id)
    date = datetime.date.today()
    text = request.form.get("comment")
    print("hello!")
    cursor.execute('''INSERT INTO Comments (user_id, date, picture_id, text) VALUES (%s, %s, %s , %s )''', (uid, date, picture_id, text))
    main.conn.commit()
    return comments(picture_id)
