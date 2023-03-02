######################################
# author ben lawson <balawson@bu.edu>
# Edited by: Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import datetime
import flask
from flask import Flask, Response, request, render_template, redirect, url_for, Blueprint
from flaskext.mysql import MySQL
import flask_login
from flask_login import current_user
from Routing.upload_handling import upload_handling
from Routing.album_creation import album_creation
from Routing.global_feed import global_feed
from Routing.personal_feed import personal_feed
from Routing.comment_handling import comment_handling
from Routing.album_viewing import album_viewing
from Routing.friends_handling import friends_handling

# for image uploading
import os
import base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'CS460'
app.register_blueprint(upload_handling)
app.register_blueprint(album_creation)
app.register_blueprint(global_feed)
app.register_blueprint(personal_feed)
app.register_blueprint(comment_handling)
app.register_blueprint(album_viewing)
app.register_blueprint(friends_handling)

# These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123321Ab!'  # ADD YOUR PASSWORD
app.config['MYSQL_DATABASE_DB'] = 'photoshare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users")
users = cursor.fetchall()



def getUserList():
    cursor = conn.cursor()
    cursor.execute("SELECT email from Users")
    return cursor.fetchall()


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    users = getUserList()
    if not (email) or email not in str(users):
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    users = getUserList()
    email = request.form.get('email')
    if not (email) or email not in str(users):
        return
    user = User()
    user.id = email
    cursor = mysql.connect().cursor()
    cursor.execute(
        "SELECT password FROM Users WHERE email = '{0}'".format(email))
    data = cursor.fetchall()
    pwd = str(data[0][0])
    user.is_authenticated = request.form['password'] == pwd
    return user


'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
    return new_page_html
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='password' id='password' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form></br>
           <a href='/'>Home</a>
               '''
    # The request method is POST (page is recieving data)
    email = flask.request.form['email']
    cursor = conn.cursor()
    # check if email is registered
    if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
        data = cursor.fetchall()
        pwd = str(data[0][0])
        if flask.request.form['password'] == pwd:
            user = User()
            user.id = email
            flask_login.login_user(user)  # okay login in user
            # protected is a function defined in this file
            return flask.redirect(flask.url_for('protected'))

    # information did not match
    return "<a href='/login'>Try again</a>\
            </br><a href='/register'>or make an account</a>"


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('hello.html', message='Logged out')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('unauth.html')
    
# you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier


@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html', supress='True')


@app.route("/register", methods=['POST'])
def register_user():
    error = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'dob' in request.form and 'first_name' in request.form and 'last_name' in request.form:
        email = request.form.get('email')
        password = request.form.get('password')
        dob = request.form.get('dob')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        hometown = request.form.get('hometown')
    else:
        error = "Missing field/s"
        print(error)
        return flask.redirect(flask.url_for('register'))

    cursor = conn.cursor()
    test = isEmailUnique(email)
    if test:
        print(cursor.execute("INSERT INTO Users (email, password, dob, first_name, last_name, gender, hometown) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}',  '{6}')".format(
            email, password, dob, first_name, last_name, gender, hometown)))
        conn.commit()
        # log user in
        user = User()
        user.id = email
        flask_login.login_user(user)
        return render_template('hello.html', name=first_name, message='Account Created!')
    else:
        print("Email in already in use!")
        return flask.redirect(flask.url_for('register'))

def getComments(uid):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT commentid, FROM Comments WHERE commentid = '{0}'".format(uid))
    return cursor.fetchall()

def getLikes(uid):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT picture_id FROM Likes WHERE user_id = '{0}'".format(uid))
    return cursor.fetchall()

def getUsersPhotos(uid):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT imgdata, picture_id, caption FROM Pictures WHERE user_id = '{0}'".format(uid))
    # NOTE return a list of tuples, [(imgdata, pid, caption), ...]
    return cursor.fetchall()

def getTags(uid):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Tags.tag_name FROM Tags JOIN Tagged ON Tagged.tag_id = Tags.tag_id WHERE Tagged.user_id = '{0}'".format(uid))
    return [row[0] for row in cursor.fetchall()]

def getFeedPhotos(uid):
    cursor = conn.cursor()
    friends = getUsersFriends(uid)
    feed_tuple = getUsersPhotos(uid)
    for i in friends:
        feed_tuple = feed_tuple + getUsersPhotos(i[0])
    return feed_tuple

def getAlbumNameFromAlbumId(album_id):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Albums WHERE album_id = '{0}'".format(album_id))
    return cursor.fetchone()[0]

def getUsersAlbums(uid):
    cursor = conn.cursor() 
    cursor.execute("SELECT album_id,name FROM Albums WHERE user_id = '{0}'".format(uid))
    return cursor.fetchall()

def getUserIdFromEmail(email):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id  FROM Users WHERE email = '{0}'".format(email))
    return cursor.fetchone()[0]

def getUsersFriends(uid):
    cursor = conn.cursor() 
    cursor.execute("SELECT user_id2 FROM Friends WHERE user_id1 = '{0}'".format(uid))
    return cursor.fetchall()

def isFriendsWith(uid, uid2):
    cursor = conn.cursor() 
    if cursor.execute("SELECT user_id2 FROM Friends WHERE user_id1 = {0} AND user_id2 = {1}".format(uid, uid2)):
        print(cursor.execute("SELECT user_id2 FROM Friends WHERE user_id1 = {0} AND user_id2 = {1}".format(uid, uid2)))
        return True
    else:
        return False

def getFirstNameFromId(id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT first_name  FROM Users WHERE user_id = '{0}'".format(id))
    return cursor.fetchone()[0]

def getEmailFromId(id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email FROM Users WHERE user_id = '{0}'".format(id))
    return cursor.fetchone()[0]
def isIdValid(id):
    # use this to check if a email has already been registered
    cursor = conn.cursor()
    if cursor.execute("SELECT user_id  FROM Users WHERE user_id = '{0}'".format(id)):
        # this means there are greater than zero entries with that email
        return True
    else:
        return False

def isEmailUnique(email):
    # use this to check if a email has already been registered
    cursor = conn.cursor()
    if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)):
        # this means there are greater than zero entries with that email
        return False
    else:
        return True
# end login code
@app.route("/likes/<int:picture_id>", methods=['GET'])
def like(picture_id):
    userid = getUserIdFromEmail(flask_login.current_user.id)
    try:
        print(cursor.execute('''INSERT INTO Likes (user_id, picture_id) VALUES (%s, %s)''', (userid, picture_id)))
        conn.commit()
        return render_template('hello.html', name=flask_login.current_user.id, message='Like added!', photos=getUsersPhotos(userid), base64=base64)
    except:
        print(cursor.execute('''DELETE FROM Likes WHERE user_id = {0} AND picture_id = {1}'''.format(userid, picture_id)))
        conn.commit()
        return render_template('hello.html', name=flask_login.current_user.id, message='Unliked image!', photos=getUsersPhotos(userid), base64=base64)

@app.route("/search_tag", methods=['POST'])
def search_tag():
    if request.method == 'POST':
        tag = request.form['tag']
        cursor = conn.cursor()
        cursor.execute(
            "SELECT p.imgdata, p.caption FROM Pictures p JOIN Tagged t ON p.picture_id = t.picture_id JOIN Tags tg ON t.tag_id = tg.tag_id WHERE tg.tag_name = %s",
            (tag,)
        )
        results = cursor.fetchall()
        return render_template('hello.html', results=results)
    else:
        return render_template('hello.html')
                           
@app.route("/display_tag", methods=['GET'])
def display_tag(picture_id):
    cursor = conn.cursor()
    cursor.execute("SELECT tag_id, picture_id FROM Tagged WHERE picture_id = {1}".format(picture_id))
    tags = cursor.fetchall()
    return render_template('hello.html', tags=tags, picture_id = picture_id)
    

@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    if request.method == 'POST':
        # Retrieve form data
        picture_id = request.form['picture_id']
        tag_name = request.form['tag_name']
        
        # Check if tag already exists
        cursor = conn.cursor()
        cursor.execute("SELECT tag_id FROM Tags WHERE tag_name = %s", (tag_name,))
        result = cursor.fetchone()
        
        if result is None:
            # Tag does not exist, so add it to Tags table
            cursor.execute("INSERT INTO Tags (tag_name) VALUES (%s)", (tag_name,))
            tag_id = cursor.lastrowid
        else:
            # Tag already exists, so retrieve its tag_id
            tag_id = result[0]
            
        # Add the tag to the Tagged table
        cursor.execute("INSERT INTO Tagged (picture_id, tag_id) VALUES (%s, %s)", (picture_id, tag_id))
        conn.commit()
        
        # Redirect to photo page
        return redirect(url_for('view_photo', picture_id=picture_id))
    else:
        # Display add tag form
        picture_id = request.args.get('picture_id')
        return render_template('hello.html', picture_id=picture_id)


@app.route('/profile')
@flask_login.login_required
def protected():
    user_id = getUserIdFromEmail(flask_login.current_user.id)
    return redirect(url_for('user_profile', user_id = user_id))
    #return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile", 
                           #photos=getUsersPhotos(getUserIdFromEmail(flask_login.current_user.id)), base64=base64)

@app.route('/profile/<int:user_id>')
def user_profile(user_id):
     if isIdValid(user_id):
        cursor.execute("SELECT name, album_id FROM Albums WHERE user_id = {0}".format(user_id))
        albums = cursor.fetchall()
        return render_template('hello.html', message="Welcome to " + getFirstNameFromId(user_id) + "'s page",  
                           photos=getUsersPhotos(user_id), base64=base64, albums = albums, user_id = user_id)
     else:
         return render_template('hello.html', message="Sorry! That user does not exist")


# begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# default page
@app.route("/", methods=['GET'])
def hello():
    return render_template('hello.html', message='Welecome to Photoshare')



if __name__ == "__main__":
    # this is invoked when in the shell  you run
    # $ python app.py
    app.run(port=5000, debug=True)
