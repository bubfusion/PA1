import datetime
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
import app as main

album_creation = Blueprint('album_creation', __name__,
                        template_folder='templates')


@album_creation.route("/album_creation", methods=['GET'])
def album():
	return render_template('album_creation.html', supress='True')

@album_creation.route("/album_creation", methods=['POST'])
@flask_login.login_required
def create_album():
	if request.method == 'POST':
		name = request.form.get('album_name')
		uid = main.getUserIdFromEmail(flask_login.current_user.id)
		date = datetime.date.today()
		cursor = main.conn.cursor()
		cursor.execute('''INSERT INTO Albums (user_id, creation_date, name) VALUES (%s, %s, %s )''', (uid, date, name))
		main.conn.commit()
		return render_template('hello.html', name=main.flask_login.current_user.id, message='Album created!')
	else:
		return render_template('hello.html', name=main.flask_login.current_user.id, message='There was an error creating an album!')

