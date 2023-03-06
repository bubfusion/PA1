#Author: Brenton Babb (babbb@bu.edu)
import datetime
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import os
import base64
import app as main
import Routing.friends_handling as friends_handling

recommended_photos = Blueprint('recommended_photos', __name__, template_folder='templates')

def getRecPhotos(uid):
    recFriends = friends_handling.friendRecs(uid)
    photos = list()
    cursor = main.conn.cursor()
    for i in range(len(recFriends)):
        print(main.getUsersPhotos(recFriends[i][2]))
        photos += (main.getUsersPhotos(recFriends[i][2]))
    return photos

@recommended_photos.route("/recommended_photos", methods=['GET'])
@flask_login.login_required
def recPhotos():
    photos = getRecPhotos(main.getUserIdFromEmail(flask_login.current_user.id))
    return render_template('recommended_photos.html', photos = photos, base64 = base64)


