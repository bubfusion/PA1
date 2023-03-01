import datetime
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import os
import base64
import app as main

upload_handling = Blueprint('upload_handling', __name__,
                        template_folder='templates')


@upload_handling.route('/upload', methods=['GET'])
@flask_login.login_required
def upload():
    uid = main.getUserIdFromEmail(flask_login.current_user.id)
    albums = main.getUsersAlbums(uid)
    return render_template("upload.html",albums=albums ) 



@upload_handling.route('/upload', methods=['POST'])
@flask_login.login_required
def upload_file():
    if request.method == 'POST':
        uid = main.getUserIdFromEmail(flask_login.current_user.id)
        imgfile = request.files['photo']
        caption = request.form.get('caption')
        photo_data = imgfile.read()
        albums = request.form.get('albums')
        cursor = main.conn.cursor()
        if albums is None:
            return render_template('hello.html', name=main.flask_login.current_user.id, message='Error uploading! Please create an album', photos=main.getUsersPhotos(uid), base64=base64)
        
        cursor.execute(
            '''INSERT INTO Pictures (imgdata, user_id, caption, album_id) VALUES (%s, %s, %s, %s)''', (photo_data, uid, caption, albums))
        main.conn.commit()
        return render_template('hello.html', name=main.flask_login.current_user.id, message='Photo uploaded!', photos=main.getUsersPhotos(uid), base64=base64)
    # The method is GET so we return a  HTML form to upload the a photo.
    else:
        return render_template('upload.html')
# end photo uploading code