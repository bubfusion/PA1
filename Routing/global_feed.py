import datetime
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import os
import base64
import app as main

global_feed = Blueprint('global_feed', __name__, template_folder='templates')

@global_feed.route('/global', methods=['GET'])
def feed():
    current_user = main.getUserIdFromEmail(flask_login.current_user.id)
    cursor = main.conn.cursor()
    cursor.execute("SELECT imgdata, picture_id, caption, user_id FROM Pictures")
    photos = list(cursor.fetchall())

    for i in range(0,len(photos)):
        photos[i] = photos[i] + (main.getNumLike(photos[i][1]),)
    print(photos)
    return render_template('hello.html', message='Global feed', photos=photos, base64=base64, current_user = current_user)