
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import os
import base64
import app as main
tag_handling = Blueprint('tag_handling', __name__, template_folder='templates')

@tag_handling.route("/tags", methods=['GET']) 
def tags():
   return render_template('tags.html')

# Adds tag to db from profiles
@tag_handling.route("/add_tag/<int:picture_id>", methods=['POST']) 
def add_tag(picture_id):
    tag_name = str(request.form.get("tag_name"))
    uid = flask_login.current_user.id
    cursor = main.conn.cursor()
    print(cursor.execute("INSERT INTO Tags (tag_id, picture_id, name) VALUES (%s, %s, %s)", (uid, picture_id, tag_name)))
    main.conn.commit()
    return render_template('hello.html', message='Tag added!', base64=base64)


@tag_handling.route('/tag_search', methods=['GET'])
def tag_search():
    return render_template('tag_search.html')

# Displays all photos from tag after tag_search        
@tag_handling.route('/tag_search', methods=['POST']) 
def display_allphotos():
    name = str(request.form.get("searched_tag"))
    cursor = main.conn.cursor()
    cursor.execute("SELECT Tags.name, Pictures.imgdata, Tags.picture_id FROM Tags INNER JOIN Pictures ON Tags.picture_id = Pictures.picture_id WHERE name  = %s", (name))
    pictures = cursor.fetchall()
    return render_template('tag_search.html', display_all=main.getUserPhotosFromPictureID(pictures))

# Displays all user photos from tag after tag_search      
@tag_handling.route('/tag_search', methods=['POST'])
def display_userphotos():
    uid = flask_login.current_user.id
    name = str(request.form.get("searched_tag"))
    cursor = main.conn.cursor()
    cursor.execute("SELECT Tags.name, Pictures.imgdata, Tags.picture_id FROM Tags INNER JOIN Pictures ON Tags.picture_id = Pictures.picture_id WHERE tag_id = %s AND name  = %s", (uid, name))
    pictures = cursor.fetchall()
    return render_template('tag_search.html', display_user=main.getUserPhotosFromPictureID(pictures)) 

#display tags on profile
@tag_handling.route("/display_tags/<int:picture_id>", methods=['GET']) 
def display_tags(picture_id):
    tags = main.getTagsFromPictureID(picture_id)
    return render_template('hello.html', display_tags = tags, base64=base64)

#display popular tags on profile
@tag_handling.route("/display_populartags/", methods=['GET']) 
def get_popular_tags():
    cursor = main.conn.cursor()
    print(cursor.execute('SELECT Tags.name, COUNT(*) as count FROM Tags JOIN Tagged ON Tags.tag_id = Tagged.tag_id GROUP BY Tags.tag_id ORDER BY count DESC LIMIT 3'))
    tags = cursor.fetchall()
    main.conn.close()
    return render_template('hello.html',popular_tags=tags, base64=base64)


