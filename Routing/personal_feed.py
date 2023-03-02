import datetime
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import os
import base64
import app as main

personal_feed = Blueprint('person_feed', __name__, template_folder='templates')

@personal_feed.route('/personal-feed', methods=['GET'])
def feed():
    current_user = main.getUserIdFromEmail(flask_login.current_user.id)
    photos = main.getFeedPhotos((current_user))
    return render_template('hello.html', message='Your feed', photos=photos, base64=base64, current_user = current_user)