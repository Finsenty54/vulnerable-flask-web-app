#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, flash, redirect, render_template, \
     request, url_for,render_template_string,make_response
from werkzeug import secure_filename
from lxml import etree
import yaml
import html
import pickle
import ssl
import jsonpickle
import json
from flask import current_app
import cgi
from base64 import b64decode,b64encode
import base64
from flask import send_from_directory
import os
import subprocess
from time import sleep
import re
import mysql.connector
from mysql.connector import errorcode
app = Flask("my-app", static_folder="static", template_folder="templates")
app.config['SECRET_KEY'] = '123456'

UPLOAD_FOLDER = os.path.dirname(__file__)+'/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql_host = "mysql"
mysql_user = "root"
mysql_pwd = "root"
mysql_db_name = "security"

_secret = 'fad08d06495532c3a'

"""
CREATE DATABASE `security` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE TABLE `security`.`users` (
`account` varchar(20) NOT NULL,
`password` varchar(20) DEFAULT NULL,
PRIMARY KEY (`account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

class User(object):

    def __init__(self, username):
        self.username = username


def type_check(password):
    counter = 0
    tip = True
    for i in range(len(_secret)):
        if not password[i] == _secret[i]:
            tip=False
        # Introduce sleep(0.1) here to run the most basic test (easily seen)
        sleep(0.1)
        counter += 1

    return tip

def get_user_file(f_name):
    with open(f_name) as f:
        return f.readlines()

app.jinja_env.globals['get_user_file'] = get_user_file

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def query_db(sql):
    db = mysql.connector.connect(host="mysql",user="root",passwd="root",database="security")
    cur = db.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
    except:
        print("error: sql:" + sql)
    cur.close()
    db.close()
    return result

def update_db(sql):
    print(sql)
    db = mysql.connector.connect(host="mysql",user="root",passwd="root",database="security")
    cur = db.cursor()
    try:
        cur.execute(sql)
    except:
        print("error: sql:" + sql)
    db.commit()
    cur.close()
    db.close()

@app.route("/create")
def create():
	db = mysql.connector.connect(host="mysql",user="root",passwd="root")
	cur=db.cursor()
	cur.execute("CREATE DATABASE security")
	db.commit()
	cur.close()
	db.close()
	return "success"

@app.route("/list")
def list():
    results = query_db(" select account,password from `security`.`users` ")
    out = "results:\n"
    for result in results:
        account = result[0]
        password = result[1]
        out += "account:" + account + ",password:" + password +"\n"
    return out

@app.route("/add")
def add():
    ''' db1 = mysql.connector.connect(host="mysql",user="root",passwd="root",database="security")
    cur1=db1.cursor()
    cur1.execute("CREATE TABLE users (account VARCHAR(20), password VARCHAR(20))")
    db1.commit()
    cur1.close()
    db1.close()'''
    sql = " insert ignore into `security`.`users`(`account`,`password` ) values ('admin','admin')"
    update_db(sql)
    return "ok"

@app.route('/hello/')
@app.route('/hello/finsenty')
def hello(name='finsenty'):
    return render_template('hello.html',name=name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sql_vulnerability',methods=('GET','POST'))
def sql_vulnerability():
    error=None
    sql_sentence=None
    success=None
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        flash(account)
        db = mysql.connector.connect(host="mysql",user="root",passwd="root",database="security")
        cur = db.cursor()
        query=("SELECT account,password FROM users"
        " WHERE account = %s")
        cur.execute(query,(account,))
        acc=cur.fetchone()
        if acc is None:
            error='Incorrect Account'
            sql_sentence="SELECT account,password FROM users WHERE account = '%s'" %account
        elif acc[1]!=password:
            error='Incorrect Password!'
        else:
            success='You were successfully log in!'
        cur.close()
        db.close()
    return render_template('sql_vulnerability.html',error=error,
    sql_sentence=sql_sentence,success=success)

@app.route('/xss_attack',methods=('GET','POST'))
def xss_attack():
    error=None
    if request.method=='POST':
        search=request.form['search']
        str1=search.replace("script","")
        str2=str1.replace("on","")
        str3=str2.replace("src","")
        str4=str3.replace("data","")
        str5=str4.replace("href","")
        #return 'can not find %s' %str5
        error='can not find %s' %str5

    return render_template('xss_attack.html',error=error)

@app.route('/upload_file',methods=('GET','POST'))
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload_file.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

@app.route('/include_file')
def include_file():
    person = {'name': "world", 'secret': "UGhldmJoZj8gYWl2ZnZoei5wYnovcG5lcnJlZg=="}
    if request.args.get('name'):
        person['name'] = request.args.get('name')
    template = '''<h2>Hello %s!</h2>''' % person['name']
    return render_template('include_file.html', person=person)


@app.route('/implement_directive',methods=('GET','POST'))
def implement_directive():
    error=None
    commandResult=None
    if request.method=='POST':
        ip= request.form["ip"]
        ippattern="(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)"
        testip=ip.split(".")
        
        if(testip[0].isdigit() and testip[1].isdigit() and testip[2].isdigit()and testip[3].isdigit()):
            current_path=os.getcwd()
            payload="python %s/templates/findip.py %s"%(current_path,ip)
            commandResult=subprocess.getoutput(payload)
        else:
            error="[-]%s ip格式不正确" %ip

        '''if(re.match(ippattern,ip)):
            current_path=os.getcwd()
            payload="python %s/templates/findip.py %s"%(current_path,ip)
            commandResult=subprocess.getoutput(payload)
        else:
            error="[-]%s ip格式不正确"%(ip) '''    
    return render_template('implement_directive.html',error=error,commandResult=commandResult)

@app.route('/xxe', methods = ['POST', 'GET'])
def xxe():
    parsed_xml = None
    file=None
    if request.method == 'POST':
        xml = request.form['xml']
        xml = xml.encode('utf-8')
        parser = etree.XMLParser(no_network=False, dtd_validation=False,resolve_entities=False)
        doc = etree.fromstring(xml, parser)
        parsed_xml =etree.tostring(doc)
        file=os.path.dirname(__file__)
    return render_template('xxe.html',parsed_xml=parsed_xml,file=file)


# deserialisation vulnerability
@app.route('/cookie', methods = ['POST', 'GET'])
def cookie():
    cookieValue = None
    value = None
    detect=None
    cookies=None
    cookies=request.cookies
    if request.method == 'POST':
        cookieValue = request.form['value']
        value = cookieValue

    if 'value' in request.cookies:
            cookieValue = pickle.loads(b64decode(value)) 
    #Decode a Base64 encoded string.
    
    #detect=pickle.loads(b64decode(request.cookies['value']))

    resp = make_response(render_template('deserialisation.html',cookieValue=str(cookieValue),detect=detect,cookies=cookies))
    
    if value and b64encode(b64decode(value)) == value:
        resp.set_cookie('value', value)
    else:
        resp.set_cookie('value', b64encode(pickle.dumps(value)))


    return resp

@app.route('/timing_attack',methods=['POST','GET'])
def timing_attack():
    password = request.args.get('password', None)
    username = request.args.get('user', 'stranger')
    err = None
    is_admin = False

    if password:
        correct_password = type_check( password)

        if correct_password and username == 'admin':
            is_admin = True
        else:
            username = 'stranger'
            err = True

    response = make_response(render_template('timing_attack.html', user=username, error=err, admin=is_admin))
    response.status_code = 500 if is_admin else 500

    return response

@app.route("/yaml_handle", methods = ['POST','GET'])
def yaml_handle():
    ydata=None
    if request.method == "POST":
        f = request.files['file']
        
        fname = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        file_path = UPLOAD_FOLDER+'/'+fname

        with open(file_path, 'r') as yfile:
            y = yfile.read()
        
        ydata =yaml.load(y)
        
    return render_template('yaml_handle.html', name = ydata)

@app.route('/json_attack')
def json_attack():
    if request.cookies.get("username"):
        a=request.cookies.get("username")
        b=a.encode('utf-8')
        if b'reduce' in base64.b64decode(b):
            return 'false'
        else:
            u = jsonpickle.decode(base64.b64decode(request.cookies.get("username")))
            return render_template("json_attack.html", username=u)
    else:
        w = redirect("/whoami")
        response = current_app.make_response(w)
        u = User("Guest")
        t=jsonpickle.encode(u)
        y=t.encode('utf-8')
        encoded = base64.b64encode(y)
        response.set_cookie("username", value=encoded)
        return response
 

@app.route('/whoami')
def whoami():
    User = jsonpickle.decode(base64.b64decode(request.cookies.get("username")))
    username = User.username
    return render_template("whoami.html", username=username)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug='true')


