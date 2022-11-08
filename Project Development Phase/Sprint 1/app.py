from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json
import requests
from watson_developer_cloud import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(_name_)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'ZzORf6jIVK'
app.config['MYSQL_PASSWORD'] = 'e6u31tnYxX'
app.config['MYSQL_DB'] = 'ZzORf6jIVK'
mysql = MySQL(app)
app.secret_key = 'a'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/uploaddata', methods=['GET', 'POST'])
def uploaddata():
    msg = ''
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['emailaddress']
        pword = request.form['pword']
        
        session["username"] = name
           
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO user VALUES (% s, % s, % s)', (name, email, pword))
        mysql.connection.commit()
        msg = 'You have successfully registered !'
    return render_template('login.html', msg=msg)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        email = request.form['emailaddress']
        pword = request.form['pword']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE email= % s', (email,))
        mysql.connection.commit()
        userexist = cursor.fetchone()
        if userexist == None:
            msg = 'User with this Email doesn\'t exist. Please Sign-up before Login'
            return render_template('login.html', msg=msg)
        cursor.execute(
            'SELECT * FROM user WHERE email= % s and password = % s', (email, pword))
        mysql.connection.commit()
        data = cursor.fetchone()
        if data == None:
            data = 'INCORRECT DETAILS'
            return render_template('login.html', msg=data)
        else:
            session["email"] = email
        print("data", data)
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

if _name_ == '_main_':
    app.run(host='0.0.0.0', debug=True,port=8080)
