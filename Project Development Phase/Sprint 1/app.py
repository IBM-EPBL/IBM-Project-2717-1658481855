from flask import Flask, render_template, request, session
import requests
import ibm_db
import bcrypt
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=wdt07473;PWD=khxUTQVy0OaDAOdc",'','')

app = Flask(_name_)
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
