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

friends_handling = Blueprint('friends_handling', __name__, template_folder='templates')


def friendTuple(uid):
    friendIds = main.getUsersFriends(uid)
    friends = []
    for i in friendIds:
        friends.append((main.getFirstNameFromId(i[0]), main.getEmailFromId(i[0]), i[0]))
    return friends

def friendRecs(uid):
    friends = friendTuple(uid)
    friendsOfFriends = set()
    for i in range(len(friends)):
        friendsOfCurrentUser = friendTuple(friends[i][2])
        for x in range(len(friendsOfCurrentUser)):
            friendsOfFriends.add(friendsOfCurrentUser[x])
    friends = set(friends)
    final = friendsOfFriends.difference(friends)
    print(final)
    return final

@friends_handling.route("/friends", methods=['GET'])
def friend():
    friends = friendTuple(main.getUserIdFromEmail(flask_login.current_user.id))
    recs = friendRecs(main.getUserIdFromEmail(flask_login.current_user.id))
    return render_template('friends.html', friends = friends, recs = recs)

@friends_handling.route('/friends', methods=['POST'])
def add_friend():
    if request.method == 'POST':
        friend = request.form.get('friends')
        uid1 = main.getUserIdFromEmail(flask_login.current_user.id)
        
        if main.isEmailUnique(friend) == True:
            return render_template('friends.html', msg = 'Email does not exist!', friends = friendTuple(flask_login.current_user.id))
        else:
             uid2 = main.getUserIdFromEmail(friend)
        if main.isFriendsWith(uid1, uid2):
            return render_template('friends.html', msg = 'You are already friends with that user', friends = friendTuple(flask_login.current_user.id))
        else:
            try:
                cursor = main.conn.cursor()
                print(cursor.execute('''INSERT INTO Friends (user_id1, user_id2) VALUES (%s, %s)''', (uid1, uid2)))
                main.conn.commit()
                return render_template('hello.html', name=flask_login.current_user.id, message='Friend added!', photos=main.getUsersPhotos(uid1), base64=base64)
            except:
                return render_template('friends.html', msg = 'Can not friend yourself!', friends = friendTuple(flask_login.current_user.id))    
    else:
        return render_template('friends.html')