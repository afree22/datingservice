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

    return render_template('signup.html', clients=clients)

@app.route('/signup_kids', methods=['GET'])
def signup_kids():
    """ Page for information on client's children
    """
    return render_template('children.html')

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
    # this html file is just a placeholder, haven't actually started this yet
    return render_template('interests.html')

@app.route('/insert_interets', methods=['POST'])
def insert_interests():
    interest = request.form['interest']
    interest_type = request.form['interest_type']
    ssn = request.form['ssn']
    if not db.check_interest(interest):
        db.add_interest(interest)
        if db.add_interest_type(interest_type):
            return redirect('/interests')
        return "Error"

    if not db.check_interest_type(interest_type):
        if db.add_interest_type(interest_type):
            return redirect('/interests')
        return "Error"

    if db.add_client_interest(ssn, interest, interest_type):
        return redirect('/interests')
    return "Error"

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

@app.route('/client_search', methods=['GET'])
def client_search():
    # return page with possible things to search for
    return render_template('client_search.html')

@app.route('/client_matches', methods=['POST'])
def client_matches():
    gender = request.form.get('gender')
    age = request.form.get('age')
    eye_color = request.form.get('eyecolor')
    weight = request.form.get('weight')
    height = request.form.get('height')
    prev_marraige = request.form.get('prior_marriage')
    interest = request.form.get('interest')
    interest_type = request.form.get('interest_type')
    
    matches = db.get_client_matches(
        gender,
        age,
        eye_color,
        weight,
        height,
        prev_marraige,
        interest,
        interest_type)
    
    return render_template('request_date.html', matches=matches)

@app.route('/make_date', methods=['POST'])
def make_date():
    user_ssn = request.form['userssn']
    date_ssn = request.form['match']

    return render_template('finalize_date.html', user_ssn=user_ssn, date_ssn=date_ssn)

@app.route('/finalize_date', methods=['POST'])
def finalize_date():
    date = request.form['date']
    location = request.form['location']
    user_ssn = request.form['user_ssn']
    date_ssn = request.form['date_ssn']

    if db.insert_date(user_ssn, date_ssn, location, date):
        return redirect('/client_search')
    return "Error"

@app.route('/date_feed', methods=['GET'])
def date_feed():
    # for now, have user enter id before clicking to go to this url?
    dates = db.get_dates()

@app.route('/client-welcome', methods=['GET'])
def client_welcome():
    return render_template('client-welcome.html')

@app.route('/specialist-login', methods=['GET'])
def specialist_login():
    return render_template('specialist-login.html')

@app.route('/staff-login', methods=['GET'])
def staff_login():
    return render_template('staff-login.html')

@app.route('/client-login', methods=['GET'])
def client_login():
    return render_template('client-login.html')

@app.route('/cli_validation', methods=['GET'])
def cli_validate():
    return render_template('client-page.html')
    #ssn = request.form['ssn']
    #if db.login_client(ssn):
    #    return render_template('client-page.html')
    #else:
    #    return render_template('client-login.html')

@app.route('/staff_validation', methods=['GET'])
def staff_validate():
    #username = request.form['username']
    #password = request.form['password']
    return render_template('staff-welcome.html')

@app.route('/specialist_validation', methods=['GET'])
def specialist_validate():
    #username = request.form['username']
    #password = request.form['password']
    return render_template('specialist-welcome.html')









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
@app.route('/all_clients', methods=['GET'])
def all_clients():
    results = db.fetch_allClients()
    return render_template('all_clients.html', results=results)

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
