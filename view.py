# original author: Luca Soldaini


# conferring of supervising privileges doesn't need to be supported by app
# users should have input on when dates happen/can just input/edit themselves


# third party modules
from flask import (Flask, render_template, request, send_from_directory, redirect)
import datetime

# project modules
import config
from logic import Database


# instanciate application and database object
app = Flask(__name__)
db = Database(config)

# configure the web app according to the config object
app.host = config.APP_HOST
app.port = config.APP_PORT
app.debug = config.APP_DEBUG


@app.route('/signup', methods=['GET'])
def signup():
    """ Sign up page
    """
    
    clients = db.get_people()

    return render_template('index2.html', clients=clients)

@app.route('/signup_kids', methods=['GET'])
def signup_kids():
    """ Page for information on client's children
    """
    return render_template('index3.html')

@app.route('/insert_client', methods=['POST'])
def insert_client():
    """ Take client info from signup and insert into db
    """
    name = request.form['name']
    phone = request.form['phone']
    dob = request.form['dob']
    ssn = request.form['ssn']
    gender = request.form['gender']
    eye_color = request.form['EyeColor']
    weight = request.form['weight']
    height = request.form['height']
    prev_marraige = request.form['PrevMarriage']
    interested_in = request.form['InterestedIn']
    open_date = str(datetime.datetime.now()).split()[0]

    if db.insert_person_(ssn, name, gender, dob, phone, eye_color, weight, height, prev_marraige, interested_in, open_date, None, "active"):
        return redirect('/signup_kids')
    return "Error"

@app.route('/interests', methods=['GET'])
def interests():

    # show interests that already exist???
    # we don't have this in the schema yet
    # this html file is just a placeholder, haven't actually started this yet
    return render_template('index4.html')

@app.route('/insert_interets', methods=['POST'])
def insert_interests():
    if db.check_interest():
        pass
        
    pass

@app.route('/insert_child', methods=['POST'])
def insert_child():
    name = request.form['name']
    dob = request.form['dob']
    status = request.form['status']
    ssn = request.form['ParentSSN']

    if db.insert_child_(ssn, name, dob, status):
        return redirect('/signup_kids')
    return "Error"

@app.route('/', methods=['GET'])
def index():
    """Get the main page"""
    people = db.get_people()
    return render_template('index.html', people=people)


@app.route('/insert', methods=['POST'])
def insert():
    """Add the person"""
    firstname, lastname = request.form['firstname'], request.form['lastname']
    phone, age = request.form['phone'], request.form['age']

    # insert person
    if db.insert_person(firstname, lastname, phone, age):
        return redirect('/')
    return "Error adding to list" # TODO: better error handling

@app.route('/resources/<path:path>')
def send_resources(path):
    return send_from_directory('resources', path)

if __name__ == '__main__':
    app.run()
