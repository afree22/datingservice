# original author: Luca Soldaini

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
def client_search():

    # show interests that already exist???
    # we don't have this in the schema yet
    # this html file is just a placeholder, haven't actually started this yet
    return render_template('index4.html')

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

@app.route('/client-welcome', methods=['GET'])
def client_welcome():
    return render_template('client-welcome.html')

@app.route('/other-login', methods=['GET'])
def other_login():
    return render_template('other-login.html')

@app.route('/client-login', methods=['GET'])
def client_login():
    return render_template('client-login.html')

@app.route('/cli_validation', methods=['GET'])
def cli_validate():
    ssn = request.form['ssn']
    if db.login_client(ssn):
        return render_template('client-page.html')
    else:
        return render_template('client-login.html')

@app.route('/other_validation', methods=['GET'])
def other_validate():
    username = request.form['username']
    password = request.form['password']
    use_type = request.form['use_type']
    if db.login_other(username,password,use_type):
        return render_template('cli_welcome.html')
    else:
        return render_template('other-login.html')







@app.route('/staff-welcome', methods=['GET'])
def staff_welcome():
    return render_template('staff-welcome.html')

@app.route('/specialist-welcome', methods=['GET'])
def specialist_welcome():
    return render_template('specialist-welcome.html')







                               
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


"""Client Match Search Results"""
@app.route('/match_results', methods=['GET'])
def match_results():
    results = db.fetch_allClients()
    return render_template('match_results.html', results=results)

@app.route('/match_search', methods=['GET'])
def match_search():
    ssn = request.args.get('SSN')
    name = request.args.get('Name')
    gender = request.args.get('Gender')
    dob = request.args.get('DOB')
    phone = request.args.get('Phone')
    eyecolor = request.args.get('eyecolor')
    weight = request.args.get('weight')
    height = request.args.get('height')
    prior_marriage = request.args.get('prior_marriage')
    interest = request.args.get('interest')
    date_open = request.args.get('date_open')
    date_close = request.args.get('date_close')
    status = request.args.get('status')
    crime = request.args.get('crime')

    results = db.fetch_potential_match(ssn,name,gender,dob,phone,eyecolor,weight,height,prior_marriage,interest, date_open, date_close, status, crime)
    return render_template('match_results.html', results=results)

if __name__ == '__main__':
    app.run()
