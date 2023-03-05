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

leader_board = Blueprint('leader_board', __name__,
                        template_folder='templates')

@leader_board.route('/leader_board', methods=['GET'])
def getLB():
    cursor = main.conn.cursor()
    cursor.execute("SELECT MAX(user_id) FROM Users")
    highest_id = cursor.fetchone()[0]
    leader_list = []

    for i in range(highest_id):
        current_id = i+1
        leader_list.append([current_id, main.getContributionScore(current_id), main.getFirstNameFromId(current_id)])

    leader_list.sort(key = lambda x: x[1], reverse=True)
    return render_template('leader_boards.html', leader_list = leader_list)