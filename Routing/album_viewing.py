import datetime
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import app as main
import base64
import os

album_viewing = Blueprint('album_viewing', __name__,
                        template_folder='templates')

@album_viewing.route('/profile/<int:user_id>/<int:album_id>', methods=['GET'])
def user_profile(user_id, album_id):
     print(user_id, album_id)
     if main.isIdValid(user_id):
        cursor = main.conn.cursor()
        cursor.execute("SELECT Pictures.imgdata, Pictures.picture_id, Pictures.caption FROM Albums INNER JOIN Pictures ON Albums.album_id = Pictures.album_id WHERE Albums.album_id = {0}".format(album_id))
        photos = cursor.fetchall()
        return render_template('hello.html', message="Album: " + main.getAlbumNameFromAlbumId(album_id),  
                           photos=photos, base64=base64, user_id = user_id)
     else:
         return render_template('hello.html', message="Sorry! That user does not exist")