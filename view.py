# conferring of supervising privileges doesn't need to be supported by app
# users should have input on when dates happen/can just input/edit themselves


# third party modules
from flask import (Flask, render_template, request, send_from_directory, redirect, make_response)
from collections import defaultdict
from datetime import datetime
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

""" THIS IS THE MAIN PAGE """
@app.route('/', methods=['GET'])
def signup():
    clients = db.get_people()
    if clients:
        return render_template('signup.html', clients=clients)
    return render_template('error')

@app.route('/error', methods=['GET'])
def error():
    return render_template('error.html')

""" Sign up client's children """
@app.route('/signup_kids', methods=['GET'])
def signup_kids():
    """ Page for information on client's children """
    return render_template('children.html')

@app.route('/insert_child', methods=['POST'])
def insert_child():
    name = request.form['name']
    dob = request.form['dob']
    status = request.form['status']
    ssn = request.form['ParentSSN']
    
    if db.insert_child_(ssn, name, dob, status):
        return redirect('/signup_kids')
    return "Error"


""" Insert a client """
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

    # have to charge registration fee at signup
    if db.insert_person_(ssn, name, gender, dob, phone, eye_color, weight, height, prev_marraige, interested_in, open_date, None, "active") and db.charge_registration_fee(ssn):
        resp = make_response(redirect('/signup_kids'))
        resp.set_cookie('userID', ssn)
        return resp
    return "Error"

""" Insert Interests """
@app.route('/interests', methods=['GET'])
def interests():
    # this html file is just a placeholder, haven't actually started this yet
    return render_template('interests.html')

@app.route('/insert_interests', methods=['POST'])
def insert_interests():
    interest = request.form['category']
    interest_type = request.form['specific']
    ssn = request.form['ssn']

    print("\n\n")
    print("interest: " + interest + " interest type " + interest_type)

    if not db.check_interest_exists(interest_type, interest):
        print("in first if")
        db.add_interest_type(interest_type, interest)
        if db.add_interest(ssn, interest_type):
            return redirect('/interests')
        return "Error"

    if db.add_interest(ssn, interest_type):
        print("in third if")
        return redirect('/interests')
    return "Error"



""" Specialist Insert Client """
@app.route('/specialist_signup_client', methods=['GET'])
def specialist_signup_client():
    return render_template('specialist-signup-client.html')

@app.route('/specialist_insert', methods=['POST'])
def specialist_insert():
    """ Specialists inserts the info into the database """
    ssn = request.form['ssn']
    name = request.form['name']
    phone = request.form['phone']
    dob = request.form['dob']
    ssn = request.form['ssn']
    gender = request.form['gender']
    eye_color = request.form['EyeColor']
    weight = request.form['weight']
    height = request.form['height']
    prior_marriage = request.form['PrevMarriage']
    interest_in = request.form['InterestedIn']
    date_open = request.form['open_date']
    date_close = request.form['close_date']
    status = request.form['status']
    if(date_close):
        if db.specialist_insert_person(ssn, name, gender, dob, phone, eye_color, weight, height, prior_marriage, interest_in, date_open, date_close, status):
                db.charge_registration_fee(ssn)
                return redirect('/specialist_add_landing')
    else:
        if db.specialist_insert_person(ssn, name, gender, dob, phone, eye_color, weight, height, prior_marriage, interest_in, date_open, None, status):
                db.charge_registration_fee(ssn)
                return redirect('/specialist_add_landing')
    return redirect('error')




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
    children = request.form.get('children')
    
    matches = db.get_client_matches(
        gender,
        age,
        eye_color,
        weight,
        height,
        prev_marraige,
        interest,
        interest_type,
        children)

    # print([i for i in matches])
    
    return render_template('request_date.html', matches=matches)

@app.route('/make_date', methods=['POST'])
def make_date():
    # user_ssn = request.form['userssn']
    print(request.form)
    user_ssn = request.cookies['userID']
    ssns = request.form['match'].split()
    date_ssn = ssns[0] if int(ssns[0]) != int(user_ssn) else ssns[1]

    print("\n")
    print("date ssn")
    print(date_ssn)
    print("user ssn")
    print(user_ssn)
    print("\n")

    return render_template('finalize_date.html', user_ssn=user_ssn, date_ssn=date_ssn)

@app.route('/finalize_date', methods=['POST'])
def finalize_date():

    # def charge(ssn):
    #     if num_matches in range(3):
    #         # no charge
    #         pass
        
    #     elif num_matches in range(3, 5):
    #         # charge
    #         db.charge_match_fee(ssn)
    #         pass

    #     elif num_matches == 6:
    #         # free match
    #         pass

    #     elif num_matches == 7:
    #         # charge registration fee
    #         db.charge_registration_fee(ssn)
    #         pass

    #     else:
    #         # charge match fee
    #         db.charge_match_fee(ssn)
    #         pass

    date = request.form['date']
    location = request.form['location']
    user_ssn = request.form['user_ssn']
    date_ssn = request.form['date_ssn']

    if db.insert_date(user_ssn, date_ssn, location, date):

        # check if 3rd, 5th, 7th

        # could limit this to the number of matches unsatisfied with
        client_matches = [i for i in db.get_client_dates(user_ssn)]
        num_matches = len(client_matches)

        print("num matches: " + str(num_matches))

        if num_matches in range(3):
            # no charge
            pass
        
        elif num_matches in range(3, 5):
            # charge
            db.charge_match_fee(user_ssn)
            pass

        elif num_matches == 6:
            # free match
            pass

        elif num_matches == 7:
            # charge registration fee
            db.charge_registration_fee(user_ssn)
            pass

        else:
            # charge match fee
            db.charge_match_fee(user_ssn)
            pass

        # need to do same thing for date

        date_matches = [i for i in db.get_client_dates(date_ssn)]
        num_matches = len(date_matches)

        if num_matches in range(3):
            # no charge
            pass
        
        elif num_matches in range(3, 5):
            # charge
            db.charge_match_fee(date_ssn)
            pass

        elif num_matches == 6:
            # free match
            pass

        elif num_matches == 7:
            # charge registration fee
            db.charge_registration_fee(date_ssn)
            pass

        else:
            # charge match fee
            db.charge_match_fee(date_ssn)
            pass

        return redirect('/client_search')
        # return "Error"
    return "Error"

@app.route('/date_history', methods=['GET'])
def date_history():
    ssn = int(request.cookies['userID'])
    # print(ssn)
    # prev_dates = db.get_prev_dates(ssn)
    prev_dates = [i for i in db.get_prev_dates(ssn)]
    future_dates = db.get_future_dates(ssn)
    again_dates = db.get_interested_dates(ssn)
    second_dates = [i for i in again_dates]

    
    future_dates = [i for i in future_dates]
    # print("future dates")
    # print([i for i in future_dates])

    # print("prev dates")
    # print([i for i in prev_dates])

    # do this so that we'll only show the form to edit upcoming dates when
    # there actually are upcoming dates
    if len(future_dates) == 0:
        future_dates = []
    if len(second_dates) == 0:
        second_dates = []
    second_dates=[]
    return render_template('date_feed.html', prev_dates=prev_dates, future_dates=future_dates, second_dates=second_dates)

@app.route('/log_payment', methods=['POST'])
def log_payment():

    # print(request.form)

    user_ssn = request.cookies.get('userID')

    # print("\n\n\n\n")

    # print(request.form)

    for fee in request.form:
        print(fee)
        db.pay_fee(user_ssn, request.form[fee])

    # print("\n\n\n\n")

    return redirect('/payment-history')

# i think this isn't used anymore
@app.route('/edit_dates', methods=['GET', 'POST'])
def edit_req_date():
    date_info = request.form['edit_req'].split()
    # date_id = date_info.split()[0]
    # date_date = date_info.split()[1]
    user_ssn = request.cookies['userID']
    date_id = date_info[0] if int(date_info[0]) != int(user_ssn) else date_info[1]
    date_date = date_info[2]

    print(user_ssn)
    print("date info " + str(date_info))

    dates = db.get_dates(user_ssn, date_id, date_date)
    print(dates)
    date = [i for i in dates][0]
    return render_template('/edit_dates.html', date=date)

@app.route('/date_occurred', methods=['POST'])
def date_occurred():
    """ Update database to show a date has occurred
    """
    # todo check this, I think it's okay but can just use cookies as well
    # user_ssn = request.form['ssn']
    user_ssn = request.cookies['userID']
    date_ssn = request.form['date_ssn'] if int(request.form['date_ssn']) != int(user_ssn) else request.form['ssn']
    date_date = request.form['date_date']
    print(user_ssn, date_ssn, date_date)

    added = db.set_date_occurred(user_ssn, date_ssn, date_date)
    print(added)

    if added:
        return redirect('/date_history')
    return "Error"

@app.route('/see_again', methods=['POST'])
def log_see_again():
    """ Update database to show that people want to see e/o again
    """
    user_ssn = request.cookies['userID']
    # date_info = request.form['date_info']
    value = 'yes' if request.form.get('see_again') == 'yes' else 'no'
    date_date = request.form['date_date']
    date_ssn = request.form['ssn1'] if int(request.form['ssn1']) != int(user_ssn) else request.form['ssn2']
    print("\n\nin see again")
    print(request.form)

    print(value)
    added = db.set_see_again(user_ssn, date_ssn, date_date, value)
    if added:
        return redirect('/date_history')
    return "Error"

@app.route('/update_date', methods=['POST'])
def log_date_update():
    new_date = request.form['new_date']
    orig_date = request.form['date_date']
    new_location = request.form['new_location']
    # user_ssn = request.form['c1_ssn']
    user_ssn = request.cookies['userID']
    date_ssn = request.form['c1_ssn'] if int(request.form['c1_ssn']) != int(user_ssn) else request.form['c2_ssn']

    if db.update_date(user_ssn, date_ssn, orig_date, new_date, new_location):
        return redirect('/date_history')
    return "Error"

@app.route('/payment-history', methods=['GET'])
def show_payments():
    user_ssn = request.cookies['userID']
    payments = [i for i in db.get_payments(user_ssn)]
    print(payments)
    print(user_ssn)
    return render_template('payment_history.html', payments=payments)

@app.route('/client-home', methods=['GET'])
def client_home():
    outstanding_payments = [i for i in db.outstanding_payment(request.cookies['userID'])]
    return render_template('client-page.html', payments=outstanding_payments)


@app.route('/client-logout', methods=['GET'])
def client_logout():
    resp = make_response(redirect('/client-login'))
    resp.set_cookie('userID', '')
    return resp


""" Other Staff Login Process """
@app.route('/staff-login', methods=['GET'])
def staff_login():
    return render_template('staff-login.html')

@app.route('/staff_validate', methods=['POST'])
def staff_validate():
    staffID = int(request.form['staffID'])
    if db.entry_login(staffID):
        return redirect('entry_view_clients')
    elif db.upper_login(staffID):
        return redirect('all_clients')
    elif db.specialist_login(staffID):
        return redirect('specialist-welcome')
    else:
        return redirect('error')


""" Client Login Process """
@app.route('/client-login', methods=['GET'])
def client_login():

    if request.cookies.get('userID'):
        return redirect('/client-home')

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




""" Landing page for specialists with options """
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

""" Specialist Update Client Information """
@app.route('/specialist_update_landing', methods=['GET'])
def specialist_update_landing():
    return render_template('specialist_update_landing.html')

@app.route('/specialist_update', methods=['GET'])
def specialist_update():
    return render_template('specialist_update.html')

@app.route('/update_client', methods=['GET','POST'])
def update_client():
    ssn = request.form.get('SSN')
    ssn_new = request.form.get('ssn_new')
    name = request.form.get('name')
    gender = request.form.get('gender')
    dob = request.form.get('DOB')
    phone = request.form.get('phone')
    eyecolor = request.form.get('eyecolor')
    weight = request.form.get('weight')
    height = request.form.get('height')
    prior_marriage = request.form.get('prior_marriage')
    interest_in = request.form.get('interest')
    date_open = request.form.get('date_open')
    date_close = request.form.get('date_close')
    status = request.form.get('status')
    if db.modify_client(ssn, ssn_new, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status):
        return redirect('specialist_success')
    return redirect('error')

@app.route('/specialist_update_children', methods=['GET'])
def specialist_update_children():
    return render_template('specialist_update_children.html')

@app.route('/update_specialist_child', methods=['POST'])
def update_specialist_child():
    ssn = int(request.form['ssn'])
    name = request.form['name']
    new_name = request.form['new_name']
    dob = request.form['new_childDOB']
    status = request.form['new_childStatus']
    if db.update_specialist_child(ssn, name, new_name, dob, status):
        return redirect('specialist_success')
    return "Error"

@app.route('/specialist_update_fees', methods=['GET'])
def specialist_update_fees():
    return render_template('specialist_update_fees.html')

@app.route('/update_specialist_fees', methods=['POST'])
def update_specialist_fees():
    ssn = int(request.form['ssn'])
    date_incurred = request.form['date_incurred']
    new_date_incurred = request.form['new_date_incurred']
    new_fee_type = request.form['new_fee_type']
    new_payment_amount = int(request.form['new_payment_amount'])
    new_fee_status = request.form['new_fee_status']

    if db.update_specialist_fees(ssn, date_incurred, new_date_incurred, new_fee_type, new_payment_amount, new_fee_status):
        return redirect('specialist_success')
    return "Error"


@app.route('/specialist_update_dates', methods=['GET'])
def specialist_update_dates():
    return render_template('specialist_update_dates.html')

@app.route('/update_specialist_dates', methods=['POST'])
def update_specialist_dates():
    c1_ssn = int(request.form['c1_ssn'])
    c2_ssn = int(request.form['c2_ssn'])
    scheduled_date = request.form['scheduled_date']
    
    updated_date = request.form['updated_c2_ssn']
    updated_scheduled_date = request.form['updated_scheduled_date']
    location = request.form['location']
    occurred = request.form['occurred']
    interested = request.form['interested']
    see_again = request.form['see_again']
    
    if db.update_specialist_dates(c1_ssn, c2_ssn, scheduled_date, updated_date, updated_scheduled_date, location, occurred, interested, see_again):
        return redirect('specialist_success')
    return "Error"





""" Specialist Add Information"""
@app.route('/specialist_add_landing', methods=['GET'])
def specialist_add_landing():
    return render_template('specialist_add_landing.html')

@app.route('/specialist_add_interests', methods=['GET'])
def specialist_add_interests():
    return render_template('specialist_add_interests.html')

@app.route('/insert_specialist_interests', methods=['POST'])
def insert_specialist_interests():
    interest = request.form['category']
    interest_type = request.form['specific']
    ssn = request.form['ssn']
    
    if not db.check_interest_exists(interest_type, interest):
        print("in first if")
        db.add_interest_type(interest_type, interest)
        if db.add_interest(ssn, interest_type):
            return redirect('specialist_success')
        return "Error"
    
    if db.add_interest(ssn, interest_type):
        print("in third if")
        return redirect('specialist_success')
    return "Error"

@app.route('/specialist_add_children', methods=['GET'])
def specialist_add_children():
    return render_template('specialist_add_children.html')

@app.route('/insert_specialist_child', methods=['POST'])
def insert_specialist_child():
    name = request.form['name']
    dob = request.form['dob']
    status = request.form['status']
    ssn = request.form['ParentSSN']
    if db.insert_child_(ssn, name, dob, status):
        return redirect('specialist_success')
    return "Error"

@app.route('/specialist_success', methods=['GET'])
def specialist_success():
    return render_template('specialist_success.html')

@app.route('/specialist_add_crime', methods=['GET'])
def specialist_add_crime():
    return render_template('specialist_add_crime.html')

@app.route('/insert_crime', methods=['POST'])
def insert_crime():
    ssn = int(request.form['ssn'])
    crime = request.form['crime']
    date_close = str(datetime.datetime.now()).split()[0]
    if db.client_no_crimes(ssn):
        db.change_client_status(ssn, date_close, "criminal_closed")
        db.insert_crime(ssn,crime)
        return redirect('specialist_success')
    else:
        db.insert_crime(ssn,crime)
        return redirect('specialist_success')
    return redirect('error')


@app.route('/specialist_add_fees', methods=['GET'])
def specialist_add_fees():
    return render_template('specialist_add_fees.html')

@app.route('/insert_fees', methods=['POST'])
def insert_fees():
    ssn = int(request.form['ssn'])
    date_incurred = request.form['date_incurred']
    fee_type = request.form['fee_type']
    payment_amount = int(request.form['payment_amount'])
    fee_status = request.form['fee_status']
    if db.insert_fees(ssn, date_incurred, fee_type, payment_amount, fee_status):
        return redirect('specialist_success')
    return redirect('error')

@app.route('/specialist_add_dates', methods=['GET'])
def specialist_add_dates():
    return render_template('specialist_add_dates.html')

@app.route('/insert_dates', methods=['POST'])
def insert_dates():
    c1_ssn = int(request.form['c1_ssn'])
    c2_ssn = int(request.form['c2_ssn'])
    location = request.form['location']
    scheduled_date = request.form['scheduled_date']
    occurred = request.form['occurred']
    interested = request.form['interested']
    see_again = request.form['see_again']
    
    if db.insert_dates(c1_ssn, c2_ssn, scheduled_date, location, occurred, interested, see_again):
        return redirect('specialist_success')
    return redirect('error')




""" Specialist Delete Information """
@app.route('/specialist_delete_landing', methods=['GET', 'POST'])
def specialist_delete_landing():
    return render_template('specialist_delete_landing.html')

@app.route('/specialist_delete', methods=['GET', 'POST'])
def specialist_delete():
    return render_template('specialist_delete.html')

@app.route('/delete_client', methods=['GET', 'POST'])
def delete_client():
    ssn = int(request.args.get('SSN'))
    
    if db.delete_client(ssn):
         return redirect('specialist_success')
    else:
        return redirect('error')

@app.route('/specialist_delete_children', methods=['GET'])
def specialist_delete_children():
    return render_template('specialist_delete_children.html')

@app.route('/delete_specialist_child', methods=['POST'])
def delete_specialist_child():
    name = request.form['name']
    ssn = request.form['ParentSSN']
    if db.delete_child(ssn, name):
        return redirect('specialist_success')
    return "Error"

@app.route('/specialist_delete_interests', methods=['GET'])
def specialist_delete_interests():
    return render_template('specialist_delete_interests.html')

@app.route('/delete_specialist_interests', methods=['POST'])
def delete_specialist_interests():
    interest = request.form['interest']
    ssn = int(request.form['ssn'])
    if db.delete_interest(ssn, interest):
        return redirect('/specialist_success')
    return redirect('error')

@app.route('/specialist_delete_crime', methods=['GET'])
def specialist_delete_crime():
    return render_template('specialist_delete_crime.html')

@app.route('/delete_crime', methods=['POST'])
def delete_crime():
    ssn = int(request.form['ssn'])
    crime = request.form['crime']
    if db.delete_crime(ssn,crime):
        if db.client_no_crimes(ssn):
            db.change_client_status(ssn, None, "active")
        return redirect('specialist_success')
    return redirect('error')


@app.route('/specialist_delete_fees', methods=['GET'])
def specialist_delete_fees():
    return render_template('specialist_delete_fees.html')

@app.route('/delete_fees', methods=['POST'])
def delete_fees():
    ssn = int(request.form['ssn'])
    date_incurred = request.form['date_incurred']
    if db.delete_fees(ssn,date_incurred):
        return redirect('specialist_success')
    return redirect('error')


@app.route('/specialist_delete_dates', methods=['GET'])
def specialist_delete_dates():
    return render_template('specialist_delete_dates.html')

@app.route('/delete_dates', methods=['POST'])
def delete_dates():
    c1_ssn = int(request.form['c1_ssn'])
    c2_ssn = int(request.form['c2_ssn'])
    scheduled_date = request.form['scheduled_date']
    if db.delete_dates(c1_ssn, c2_ssn, scheduled_date):
        return redirect('specialist_success')
    return redirect('error')






""" Specialist Queries """
@app.route('/specialist_query', methods=['GET'])
def specialist_query():
    return render_template('specialist_query.html')

@app.route('/num_dates', methods=['GET'])
def num_dates():
    return render_template('num_dates.html')

@app.route('/num_dates_search', methods=['GET'])
def num_dates_search():
    comparision = request.args.get('comparision')
    number = int(request.args.get('number'))
    s1 = 'exactly'
    s2 = 'at least'
    s3 = 'at most'
    if comparision == s1:
        results = db.num_dates_exactly(number)
        return render_template('num_dates_results.html', results=results)
    elif comparision == s2:
        results = db.num_dates_atLeast(number)
        return render_template('num_dates_results.html', results=results)
    elif comparision == s3:
        results = db.num_dates_atMost(number)
        return render_template('num_dates_results.html', results=results)
    else:
        return redirect('error')

@app.route('/num_clients_married', methods=['GET'])
def num_clients_married():
    results = db.get_num_clients_married()
    if results:
        return render_template('num_clients_married.html', results=results)
    return redirect('error')

@app.route('/num_clients_gender', methods=['GET'])
def num_clients_gender():
    results = db.get_num_clients_gender()
    if results:
        return render_template('num_clients_gender.html', results=results)
    return redirect('error')

@app.route('/num_dates_gender', methods=['GET'])
def num_dates_gender():
    results = db.get_num_dates_gender()
    if results:
        results = {'male': results[0], 'female': results[1]}
        return render_template('num_dates_gender.html', results=results)
    return redirect('error')

@app.route('/type_crime', methods=['GET'])
def type_crime():
    results = db.get_type_crime()
    if results:
        return render_template('type_crime.html', results=results)
    return redirect('error')

@app.route('/age_children', methods=['GET'])
def age_children():
    currentDate = str(datetime.datetime.now()).split()[0]
    results = db.get_age_children(currentDate)
    if results:
        return render_template('age_children.html', results=results)
    return redirect('error')

@app.route('/outstanding_balance', methods=['GET'])
def outstanding_balance():
    results = db.get_outstanding_balance()
    if results:
        return render_template('outstanding_balance.html', results=results)
    return redirect('error')

@app.route('/display_interests', methods=['GET'])
def display_interests():
    results = db.display_interests()
    if results:
        return render_template('display_interests.html', results=results)
    return redirect('error')

@app.route('/average_dates_couple', methods=['GET'])
def average_dates_couple():
    results = db.average_dates_couple()
    if results:
        return render_template('average_dates_couple.html', results=results)
    return redirect('error')


""" Entry Level  Search """
@app.route('/entry_view_clients', methods=['GET'])
def entry_view_clients():
    results = db.fetch_staffClients()
    if results:
        return render_template('entry-view-clients.html', results=results)
    return redirect('error')

@app.route('/entry_search', methods=['GET','POST'])
def entry_search():
    name = request.form.get('name')
    gender = request.form.get('gender')
    dob = request.form.get('dob')
    eyecolor = request.form.get('eyecolor')
    weight = request.form.get('weight')
    height = request.form.get('height')
    prior_marriage = request.form.get('PrevMarriage')
    interest_in = request.form.get('interest_in')
    date_open = request.form.get('open_date')
    date_close = request.form.get('close_date')
    status = request.form.get('status')
    crime = request.form.get('crime')
    childName = request.form.get('childName')
    childDOB = request.form.get('childDOB')
    childStatus = request.form.get('childStatus')
    
    interest = request.form.get('interest')
    category = request.form.get('category')
    date_incurred = request.form.get('date_incurred')
    fee_type = request.form.get('fee_type')
    payment_amount = request.form.get('payment_amount')
    fee_status = request.form.get('fee_status')
    date_ssn = request.form.get('date_ssn')
    location = request.form.get('location')
    scheduled_date = request.form.get('scheduled_date')
    occurred = request.form.get('occurred')
    interested = request.form.get('interested')
    see_again = request.form.get('see_again')
    
    results = db.fetch_staff_match(name, gender, dob, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status, crime, childName, childDOB, childStatus, interest, category, date_incurred, fee_type, payment_amount, fee_status, location, scheduled_date, occurred, interested, see_again)
    if results:
        return render_template('entry-results.html', results=results)
    return render_template('error.html')



"""Client Match Search Results"""
@app.route('/all_clients', methods=['GET'])
def all_clients():
    results = [i for i in db.fetch_allClients()]
    for i in results:
        print(i)
        print("\n")
    # print(results)

    if not results:
        return render_template('error.html')


    attrs = [i for i in results[0] if i != 'ssn']
    multi_valued = set(
        ['childName', 
        'childDOB', 
        'childStatus', 
        'interest', 
        'category',
        'scheduled_date',
        'location',
        'occurred',
        'interested', 
        'see_again', 
        'date_ssn',
        'date_incurred',
        'fee_type',
        'fee_status',
        'payment_amount',
        'status',
        'crime']
    )

    clients_grouped = {i['ssn']: {
        'childName': [],
        'childDOB': [],
        'childStatus': [],
        'interest': [],
        'category': [],
        'scheduled_date': [],
        'location': [],
        'occurred': [],
        'interested': [],
        'see_again': [],
        'date_ssn': [],
        'fee_type': [],
        'payment_amount': [],
        'date_incurred': [],
        'fee_status': [],
        'crime': []
    } for i in results}

    dates = {}
    children = {}
    fees = {}
    crimes = {i['ssn']: [] for i in results}
    interests = {}
    joined = {i['ssn']: {} for i in results}

    for client in results:
        ssn = client['ssn']
        if client.get('childName'):
            child_key = (ssn, client['childName'])
            children[child_key] = {'childDOB': client['childDOB'], 'childStatus': client['childStatus']}


            # if client['childName'] not in clients_grouped[ssn]['childName']:
            #     for attr in child_attrs:
            #         clients_grouped[ssn][attr].append(client[attr])
                # clients_grouped[ssn]['childName'].append(client['childName'])
                # clients_grouped[ssn]['childDOB'].append(client['childDOB'])
                # clients_grouped[ssn]['childStatus'].append(client['childStatus'])



        if client.get('category'):
            interest_key = (ssn, client['interest'])
            interests[interest_key] = {'category': client['category']}


            # if client['category'] not in clients_grouped[ssn]['category']:
            #     for attr in interest_attrs:
            #         clients_grouped[ssn][attr].append(client[attr])
                    # interest_key = (ssn, client['interest'])
                    # interests[interest_key] = client['category']
                    # interests[ssn][attr].append(client[attr])
                # clients_grouped[ssn]['category'].append(client['category'])
                # clients_grouped[ssn]['interest'].append(client['interest'])



        if client.get('location'):
            date_key = (client['c1_ssn'], client['c2_ssn'], client['scheduled_date'])
            # dates[date_key] = (client['location'], client['interested'], client['see_again'])
            dates[date_key] = {'location': client['location'], 'interested': client['interested'], 'see_again': client['see_again']}



        if client.get('crime'):
            crimes[ssn].append(client['crime'])

            # clients_grouped[ssn]['crime'].append(client['crime'])

        if client.get('fee_type'):
            fee_key = (ssn, client['date_incurred'])
            fees[fee_key] = {
                'fee_type': client['fee_type'], 
                'payment_amount': client['payment_amount'],
                'fee_status': client['fee_status']}


            # clients_grouped[ssn]['fee_type'].append(client['fee_type'])
            # clients_grouped[ssn]['payment_amount'].append(client['payment_amount'])
            # clients_grouped[ssn]['payment_amount'].append(client['payment_amount'])

        for attr in client:
            if attr in multi_valued:
                continue
            clients_grouped[ssn][attr] = client[attr]

    # print(clients_grouped)

    for date in dates:
        clients_grouped[date[0]]['scheduled_date'].append(date[-1].strftime('%m/%d/%Y'))
        clients_grouped[date[0]]['date_ssn'].append((date[0], date[1]))
        clients_grouped[date[0]]['location'].append(dates[date]['location'])

        if dates[date]['interested']:
            clients_grouped[date[0]]['interested'].append(dates[date]['interested'])
        else:
            clients_grouped[date[0]]['interested'].append('N/A')
        if dates[date]['see_again']:
            clients_grouped[date[0]]['see_again'].append(dates[date]['see_again'])
        else:
            clients_grouped[date[0]]['see_again'].append('N/A')

        clients_grouped[date[1]]['scheduled_date'].append(date[-1].strftime('%m/%d/%Y'))
        clients_grouped[date[1]]['date_ssn'].append((date[0], date[1]))
        clients_grouped[date[1]]['location'].append(dates[date]['location'])

        if dates[date]['interested']:
            clients_grouped[date[1]]['interested'].append(dates[date]['interested'])
        else:
            clients_grouped[date[1]]['interested'].append('N/A')
        if dates[date]['see_again']:
            clients_grouped[date[1]]['see_again'].append(dates[date]['see_again'])
        else:
            clients_grouped[date[1]]['see_again'].append('N/A')

    for interest in interests:
        clients_grouped[interest[0]]['interest'].append(interest[-1])
        clients_grouped[interest[0]]['category'].append(interests[interest]['category'])

    for fee in fees:
        clients_grouped[fee[0]]['date_incurred'].append(fee[-1])
        clients_grouped[fee[0]]['fee_type'].append(fees[fee]['fee_type'])
        clients_grouped[fee[0]]['payment_amount'].append(fees[fee]['payment_amount'])
        clients_grouped[fee[0]]['fee_status'].append(fees[fee]['fee_status'])

    for child in children:
        clients_grouped[child[0]]['childName'].append(child[-1])
        clients_grouped[child[0]]['childDOB'].append(children[child]['childDOB'].strftime('%m/%d/%Y'))
        clients_grouped[child[0]]['childStatus'].append(children[child]['childStatus'])

    for crime in crimes:
        clients_grouped[crime]['crime'].extend(crimes[crime])

    # for client in clients_grouped.values():
    #     if client['childName']:
    #         client['childName'] = ', '.join(client['childName'])
    #         client['childDOB'] = ', '.join(client['childDOB'])
    #         client['childStatus'] = ', '.join(client['childStatus'])
    #     else:
    #         client['childName'] = 'N/A'
    #         client['childDOB'] = 'N/A'
    #         client['childStatus'] = 'N/A'
    #     if client['category']:
    #         client['category'] = ', '.join(client['category'])
    #         client['interest'] = ', '.join(client['interest'])
    #     else:
    #         client['category'] = 'N/A'
    #         client['interest'] = 'N/A'
    #     if client['scheduled_date']:
    #         client['scheduled_date'] = ', '.join(client['scheduled_date'])
    #         client['location'] = ', '.join(client['location'])
    #         client['occurred'] = ', '.join(client['occurred'])
    #         client['interested'] = ', '.join(client['interested'])
    #     else:
    #         client['scheduled_date'] = 'N/A'
    #         # client['c1_ssn'] = 'N/A'
    #         # client['c2_ssn'] = 'N/A'
    #         client['date_ssn'] = 'N/A'
    #         client['location'] = 'N/A'
    #         client['occurred'] = 'N/A'
    #         client['interested'] = 'N/A'
    #         client['date_ssn'] = 'N/A'

    return render_template('all_clients.html', results=clients_grouped.values())
    # return render_template('all_clients.html', results=results)

@app.route('/match_search', methods=['GET','POST'])
def match_search():
    ssn = request.args.get('ssn')
    name = request.args.get('name')
    gender = request.args.get('gender')
    dob = request.args.get('dob')
    phone = request.args.get('phone')
    eyecolor = request.args.get('eyecolor')
    weight = request.args.get('weight')
    height = request.args.get('height')
    prior_marriage = request.args.get('PrevMarriage')
    interest_in = request.args.get('interest_in')
    date_open = request.args.get('open_date')
    date_close = request.args.get('close_date')
    status = request.args.get('status')
    crime = request.args.get('crime')
    childName = request.args.get('childName')
    childDOB = request.args.get('childDOB')
    childStatus = request.args.get('childStatus')
    
    interest = request.args.get('interest')
    category = request.args.get('category')
    date_incurred = request.args.get('date_incurred')
    fee_type = request.args.get('fee_type')
    payment_amount = request.args.get('payment_amount')
    fee_status = request.args.get('fee_status')
    location = request.args.get('location')
    scheduled_date = request.args.get('scheduled_date')
    occurred = request.args.get('occurred')
    interested = request.args.get('interested')
    see_again = request.args.get('see_again')

    results = db.fetch_potential_match(ssn, name, gender, dob, phone, eyecolor, weight, height, prior_marriage, interest_in, date_open, date_close, status, crime, childName, childDOB, childStatus, interest, category, date_incurred, fee_type, payment_amount, fee_status, location, scheduled_date, occurred, interested, see_again)
    """
    results = [i for i in results]
    
    print(results)
    print("\n")
    print([i['ssn'] for i in results])
    
    attrs = [i for i in results[0] if i != 'ssn']
    multi_valued = set(
                       ['childName',
                        'childDOB',
                        'childStatus',
                        'interest',
                        'category',
                        'scheduled_date',
                        'location',
                        'occurred',
                        'interested',
                        'see_again',
                        'date_ssn',
                        'date_incurred',
                        'fee_type',
                        'fee_status',
                        'payment_amount',
                        'status',
                        'crime']
                       )
        
    clients_grouped = {i['ssn']: {
                           'childName': [],
                           'childDOB': [],
                           'childStatus': [],
                           'interest': [],
                           'category': [],
                           'scheduled_date': [],
                           'location': [],
                           'occurred': [],
                           'interested': [],
                           'see_again': [],
                           'date_ssn': [],
                           'fee_type': [],
                           'payment_amount': [],
                           'date_incurred': [],
                           'fee_status': [],
                           'crime': []
                       } for i in results}

    dates = {}
    children = {}
    fees = {}
    crimes = {i['ssn']: [] for i in results}
    interests = {}
    joined = {i['ssn']: {} for i in results}

    #print(clients_grouped)
    
    for client in results:
        ssn = client['ssn']
        if client.get('childName'):
            child_key = (ssn, client['childName'])
            children[child_key] = {'childDOB': client['childDOB'], 'childStatus': client['childStatus']}
        
        
        # if client['childName'] not in clients_grouped[ssn]['childName']:
        #     for attr in child_attrs:
        #         clients_grouped[ssn][attr].append(client[attr])
        # clients_grouped[ssn]['childName'].append(client['childName'])
        # clients_grouped[ssn]['childDOB'].append(client['childDOB'])
        # clients_grouped[ssn]['childStatus'].append(client['childStatus'])
        
        
        
        if client.get('category'):
            interest_key = (ssn, client['interest'])
            interests[interest_key] = {'category': client['category']}
        
        
        # if client['category'] not in clients_grouped[ssn]['category']:
        #     for attr in interest_attrs:
        #         clients_grouped[ssn][attr].append(client[attr])
        # interest_key = (ssn, client['interest'])
        # interests[interest_key] = client['category']
        # interests[ssn][attr].append(client[attr])
        # clients_grouped[ssn]['category'].append(client['category'])
        # clients_grouped[ssn]['interest'].append(client['interest'])
        
        
        
        if client.get('location'):
            date_key = (client['c1_ssn'], client['c2_ssn'], client['scheduled_date'])
            # dates[date_key] = (client['location'], client['interested'], client['see_again'])
            dates[date_key] = {'location': client['location'], 'interested': client['interested'], 'see_again': client['see_again']}
        
        
        
        if client.get('crime'):
            crimes[ssn].append(client['crime'])
    
        # clients_grouped[ssn]['crime'].append(client['crime'])
        
        if client.get('fee_type'):
            fee_key = (ssn, client['date_incurred'])
            fees[fee_key] = {
                'fee_type': client['fee_type'],
                'payment_amount': client['payment_amount'],
                'fee_status': client['fee_status']}
        

        # clients_grouped[ssn]['fee_type'].append(client['fee_type'])
        # clients_grouped[ssn]['payment_amount'].append(client['payment_amount'])
        # clients_grouped[ssn]['payment_amount'].append(client['payment_amount'])
        
        for attr in client:
            if attr in multi_valued:
                continue
            clients_grouped[ssn][attr] = client[attr]

    print(dates)

    for date in dates:
        clients_grouped[date[0]]['scheduled_date'].append(date[-1].strftime('%m/%d/%Y'))
        clients_grouped[date[0]]['date_ssn'].append((date[0], date[1]))
        clients_grouped[date[0]]['location'].append(dates[date]['location'])
        
        if dates[date]['interested']:
            clients_grouped[date[0]]['interested'].append(dates[date]['interested'])
        else:
            clients_grouped[date[0]]['interested'].append('N/A')
        if dates[date]['see_again']:
            clients_grouped[date[0]]['see_again'].append(dates[date]['see_again'])
        else:
            clients_grouped[date[0]]['see_again'].append('N/A')

        clients_grouped[date[1]]['scheduled_date'].append(date[-1].strftime('%m/%d/%Y'))
        clients_grouped[date[1]]['date_ssn'].append((date[0], date[1]))
        clients_grouped[date[1]]['location'].append(dates[date]['location'])

        if dates[date]['interested']:
            clients_grouped[date[1]]['interested'].append(dates[date]['interested'])
        else:
            clients_grouped[date[1]]['interested'].append('N/A')
        if dates[date]['see_again']:
            clients_grouped[date[1]]['see_again'].append(dates[date]['see_again'])
        else:
            clients_grouped[date[1]]['see_again'].append('N/A')

    for interest in interests:
        clients_grouped[interest[0]]['interest'].append(interest[-1])
        clients_grouped[interest[0]]['category'].append(interests[interest]['category'])

    for fee in fees:
        clients_grouped[fee[0]]['date_incurred'].append(fee[-1])
        clients_grouped[fee[0]]['fee_type'].append(fees[fee]['fee_type'])
        clients_grouped[fee[0]]['payment_amount'].append(fees[fee]['payment_amount'])
        clients_grouped[fee[0]]['fee_status'].append(fees[fee]['fee_status'])

    for child in children:
        clients_grouped[child[0]]['childName'].append(child[-1])
        clients_grouped[child[0]]['childDOB'].append(children[child]['childDOB'].strftime('%m/%d/%Y'))
        clients_grouped[child[0]]['childStatus'].append(children[child]['childStatus'])

    for crime in crimes:
        clients_grouped[crime]['crime'].extend(crimes[crime]) """

    return render_template('match_results.html', results=results)

if __name__ == '__main__':
    app.run()
