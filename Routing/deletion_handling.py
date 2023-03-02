import datetime
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import os
import base64
import app as main

deletion_handling = Blueprint('deletion_handling', __name__, template_folder='templates')

@deletion_handling.route('/<int:picture_id>/delete', methods=['GET'])
def delete_photo(picture_id):
    cursor = main.conn.cursor()
    print(picture_id)
    cursor.execute("SELECT user_id FROM Pictures WHERE picture_id = {0}".format(picture_id))
    picture_author = cursor.fetchone()[0]
    print(main.getUserIdFromEmail(flask_login.current_user.id), picture_author)
    if main.getUserIdFromEmail(flask_login.current_user.id) == picture_author:
        cursor.execute("DELETE FROM Pictures WHERE picture_id = {0}".format(picture_id))
        main.conn.commit
        return render_template('hello.html', message = "Photo succesfully deleted!")
    else:
        return render_template('hello.html', message = "Only author can delete photos")
