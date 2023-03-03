from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import os
import base64
import app as main
tag_handling = Blueprint('tag_handling', __name__, template_folder='templates')
# Displays all photos from tag search  
def search_tag():
    if request.method == 'POST':
        tag = request.form['tag']
        cursor = main.conn.cursor()
        cursor.execute(
            "SELECT p.imgdata, p.caption FROM Pictures p JOIN Tagged t ON p.picture_id = t.picture_id JOIN Tags tg ON t.tag_id = tg.tag_id WHERE tg.tag_name = %s",
            (tag,)
        )
        results = cursor.fetchall()
        return render_template('tags.html', results=results)
    else:
        return render_template('tags.html')

# Displays all photos from tag                        
def display_tag(picture_id):
    cursor = main.conn.cursor()
    cursor.execute("SELECT tag_id, picture_id FROM Tagged WHERE picture_id = {1}".format(picture_id))
    tags = cursor.fetchall()
    return render_template('tags.html', display_all=tags, picture_id = picture_id)

# Displays all user photos from tag  
def display_usertag(picture_id):
    cursor = main.conn.cursor()
    cursor.execute("SELECT tag_id, picture_id FROM Tagged JOIN Pictures ON Pictures.picture_id = Tagged.picture_id WHERE Pictures.user_id = %s AND Tagged.picture_id = %s", (flask_login.current_user.id, picture_id))
    tags = cursor.fetchall()
    return render_template('tags.html', display_user=tags, picture_id=picture_id) 

# Adds tag to db
def add_tag():
    tag_name = request.form['tag_name']
    picture_id = request.form['picture_id']

    # Insert tag into Tags table
    cursor = main.conn.cursor()
    cursor.execute("INSERT INTO Tags (name) VALUES (%s)", (tag_name,))
    tag_id = cursor.fetchall()

    # Associate tag with picture in Tagged table
    cursor.execute("INSERT INTO Tagged (picture_id, tag_id) VALUES (%s, %s)", (picture_id, tag_id))
    main.conn.commit()

    return render_template('tags.html')
                           
def popular_tags():
    cur = main.conn.cursor()

    cur.execute("""
        SELECT Tags.name, COUNT(*) as tag_count FROM Tagged INNER JOIN Tags ON Tagged.tag_id = Tags.tag_id GROUP BY Tags.name ORDER BY tag_count DESC LIMIT 3;
    """)

    popular_tags = cur.fetchall()
    return render_template('tags.html', popular_tags=popular_tags)