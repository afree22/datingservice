# conferring of supervising privileges doesn't need to be supported by app
# users should have input on when dates happen/can just input/edit themselves


# third party modules
from flask import (Flask, render_template, request, send_from_directory, redirect, make_response)
import datetime

# project modules
import config
from logic import Database


""" 
fees: if 5 dates don't work out, get registration charge, but don't
pay for matches if you don't like the person ???
or is it that you just get a free match if you don't like the person after two dates?
remember to add option to search by having children or not
Eugene says the string formatting thing is okay as is
"""


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
    # user_ssn = request.form['userssn']
    user_ssn = request.cookies['userID']
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

@app.route('/date_history', methods=['GET'])
def date_history():
    ssn = request.cookies['userID']
    # dates = db.get_dates(ssn)
    prev_dates = db.get_prev_dates(ssn)
    future_dates = db.get_future_dates(ssn)

    # do this so that we'll only show the form to edit upcoming dates when
    # there actually are upcoming dates
    future_dates = [i for i in future_dates]
    if len(future_dates) == 0:
        future_dates = []
    return render_template('date_feed.html', prev_dates=prev_dates, future_dates=future_dates)

@app.route('/edit_dates', methods=['GET', 'POST'])
def edit_req_date():
    date_info = request.form['edit_req']
    date_id = date_info.split()[0]
    date_date = date_info.split()[1]
    user_ssn = request.cookies['userID']

    dates = db.get_dates(user_ssn, date_id, date_date)
    date = [i for i in dates][0]
    return render_template('/edit_dates.html', date=date)

@app.route('/date_occurred', methods=['POST'])
def date_occurred():
    """ Update database to show a date has occurred
    """
    # todo check this, I think it's okay but can just use cookies as well
    c1_ssn = request.form['c1_ssn']
    c2_ssn = request.form['c2_ssn']

    added = db.set_date_occurred(c1_ssn, c2_ssn)

    if added:
        return redirect('/date_history')
    return "Error"

@app.route('/see_again', methods=['POST'])
def log_see_again():
    """ Update database to show that people want to see e/o again
    """
    c1_ssn = request.cookies['userID']
    date_info = request.form['date_info']
    print(date_info)
    c2_ssn = date_info.split()[0]
    date_date = date_info.split()[1]
    
    added = db.set_see_again(c1_ssn, c2_ssn)

    if added:
        return redirect('/date_history')
    return "Error"

@app.route('/client-welcome', methods=['GET'])
def client_welcome():
    return render_template('client-welcome.html')

@app.route('/client-home', methods=['GET'])
def client_home():
    return render_template('client-page.html')

""" Specialist Login Process """
@app.route('/specialist-login', methods=['GET'])
def specialist_login():
    return render_template('specialist-login.html')

@app.route('/specialist_validation', methods=['GET'])
def specialist_validate():
    #username = request.form['username']
    #password = request.form['password']
    return render_template('specialist-welcome.html')

""" Entry Staff Login Process """
@app.route('/entry_login', methods=['GET'])
def entry_login():
    return render_template('entry_login.html')

@app.route('/entry_validate', methods=['GET'])
def entry_validate():
    #username = request.form['username']
    #password = request.form['password']
    return redirect('entry_view_clients')

""" Other Staff Login Process """
@app.route('/staff_login', methods=['GET'])
def staff_login():
    return render_template('staff_login.html')

@app.route('/staff_validate', methods=['GET'])
def staff_validate():
    username = request.form['username']
    password = request.form['password']
    if db.login_staff(username, password):
        resp = make_response(redirect('/all_clients'))
        resp.set_cookie('userID', str(username))
        return resp
    else:
        return redirect('/staff_login')

""" Client Login Process """
@app.route('/client-login', methods=['GET'])
def client_login():
    return render_template('client-login.html')

@app.route('/cli_validation', methods=['POST'])
def cli_validate():
    # return render_template('client-page.html')
    # import pdb; pdb.set_trace()
    # pass
    ssn = request.form['ssn']
    if db.login_client(ssn):
        resp = make_response(redirect('/client-home'))
        resp.set_cookie('userID', str(ssn))
        return resp
        # return render_template('client-page.html')
    else:
       # return render_template('client-login.html')
       return redirect('/client-login')

@app.route('/logout', methods=['GET'])
def get_logout():
    # Clear the user cookie to log them out
    resp = make_response(redirect('/client-login'))
    resp.set_cookie('userID', '')
    return resp






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
    return render_template('error.html')
    #return "Error adding to list" # TODO: better error handling

@app.route('/resources/<path:path>')
def send_resources(path):
    return send_from_directory('resources', path)

""" Specialist Add Client """
@app.route('/specialist_add', methods=['GET'])
def specialist_add():
    return render_template('specialist_add.html')

@app.route('/add_new_client', methods=['GET'])
def add_new_client():
    ssn = request.args.get('SSN')
    name = request.args.get('Name')
    gender = request.args.get('Gender')
    dob = request.args.get('DOB')
    phone = request.args.get('phone')
    eyecolor = request.args.get('eyecolor')
    weight = request.args.get('weight')
    height = request.args.get('height')
    prior_marriage = request.args.get('prior_marriage')
    interest = request.args.get('interest')
    date_open = request.args.get('date_open')
    date_close = request.args.get('date_close')
    status = request.args.get('status')
    crime = request.args.get('crime')
    db.insert_client(ssn,name,gender,dob,phone,eyecolor,weight,height,prior_marriage,interest, date_open, date_close, status)
    db.insert_crime(ssn,crime)
    return redirect('specialist_success')
    return render_template('error.html')

""" Specialist Modify Client """
@app.route('/specialist_update', methods=['GET'])
def specialist_update():
    return render_template('specialist_update.html')

@app.route('/update_client', methods=['GET'])
def update_client():
    ssn = request.args.get('SSN')
    ssn_new = request.args.get('ssn_new')
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
    childName = request.args.get('childName')
    childDOB = request.args.get('childDOB')
    childStatus = request.args.get('childStatus')
    if db.modify_client(ssn,ssn_new,name,gender,dob,phone,eyecolor,weight,height,prior_marriage,interest, date_open, date_close, status, crime, childName, childDOB, childStatus):
         return redirect('specialist_success')
    return redirect('error')

@app.route('/specialist_success', methods=['GET'])
def specialist_success():
    return render_template('specialist_success.html')

""" Specialist Delete Client """
@app.route('/specialist_delete', methods=['GET'])
def specialist_delete():
    return render_template('specialist_delete.html')

@app.route('/delete_client', methods=['POST'])
def delete_client():
    ssn = request.args.get('ssn')
    if db.delete_client(ssn):
         return redirect('specialist_success')
    else:
        return redirect('error')

""" Specialist Queries """
@app.route('/specialist_query', methods=['GET'])
def specialist_query():
    return render_template('specialist_query.html')

@app.route('/num_clients_married', methods=['GET'])
def num_clients_married():
    results = db.get_num_clients_married()
    return render_template('num_clients_married.html', results=results)

@app.route('/num_clients_gender', methods=['GET'])
def num_clients_gender():
    results = db.get_num_clients_gender()
    return render_template('num_clients_gender.html', results=results)



""" Staff Search """
@app.route('/entry_view_clients', methods=['GET'])
def entry_view_clients():
    results = db.fetch_staffClients()
    return render_template('entry_view_clients.html', results=results)

@app.route('/entry_search', methods=['GET'])
def entry_search():
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
    childName = request.args.get('childName')
    childDOB = request.args.get('childDOB')
    childStatus = request.args.get('childStatus')
    
    results = db.fetch_staff_match(name,gender,dob, eyecolor,weight,height,prior_marriage,interest, date_open, date_close, status, crime, childName, childDOB, childStatus)
    return render_template('entry_results.html', results=results)


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
    childName = request.args.get('childName')
    childDOB = request.args.get('childDOB')
    childStatus = request.args.get('childStatus')

    results = db.fetch_potential_match(ssn,name,gender,dob,phone,eyecolor,weight,height,prior_marriage,interest, date_open, date_close, status, crime, childName, childDOB, childStatus)
    return render_template('match_results.html', results=results)

if __name__ == '__main__':
    app.run()
