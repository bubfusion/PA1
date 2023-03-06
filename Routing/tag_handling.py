
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
   """  tags = get_popular_tags()
    return render_template('tags.html',popular_tags=tags, base64=base64) """
   return render_template('tags.html')

def get_popular_tags():
    cursor = main.conn.cursor()
    print(cursor.execute('SELECT Tags.name, COUNT(*) as count FROM Tags JOIN Tagged ON Tags.tag_id = Tagged.tag_id GROUP BY Tags.tag_id ORDER BY count DESC LIMIT 3'))
    tags = cursor.fetchall()
    main.conn.close()
    return render_template('tags.html',popular_tags=tags, base64=base64)

# Adds tag to db
@tag_handling.route("/add_tag/<int:picture_id>", methods=['POST']) 
def add_tag(picture_id):
    tag_name = request.form["tag_name"]
    uid = flask_login.current_user.id
    # Insert tag into Tags table
    cursor = main.conn.cursor()
    print(cursor.execute("INSERT INTO Tags (tag_id, picture_id, name) VALUES (%s, %s)", (uid, picture_id, tag_name)))
    """ tag_id = cursor.fetchall()

    # Associate tag with picture in Tagged table
    print(cursor.execute("INSERT INTO Tagged (picture_id, tag_id) VALUES (%s, %s)", (picture_id, tag_id))) """
    main.conn.commit()
    tags = display_tags(picture_id)
    return render_template('hello.html', display_tags = tags, message='Tag added!', base64=base64)

# Displays all photos from tag          
tag_handling.route('tag_search', methods=['POST']) 
def display_allphotos():
    name = str(request.form.get("tag"))
    cursor = main.conn.cursor()
    cursor.execute("SELECT picture_id FROM Tags WHERE name  = %s", (name))
    pictures = cursor.fetchall()
    return render_template('tag_search.html', display_all=pictures)

# Displays all user photos from tag  
tag_handling.route('tag_search', methods=['POST'])
def display_userphotos():
    uid = flask_login.current_user.id
    name = str(request.form.get("tag"))
    cursor = main.conn.cursor()
    cursor.execute("SELECT picture_id FROM Tags WHERE tag_id = %s AND name  = %s", (uid, name))
    pictures = cursor.fetchall()
    return render_template('tag_search.html', display_user=pictures) 

#display tags to profile pictures
def display_tags(picture_id):
    tagNames = []
    tags = main.getTagsFromPictureID(picture_id)
    for i in tags:
        tagNames.append(i)
    return tagNames

