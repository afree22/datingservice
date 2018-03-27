# original author: Luca Soldaini

# third party modules
from flask import (Flask, render_template, request, send_from_directory, redirect)

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
    
    # name = request.form['Name']

    return render_template('index2.html')

@app.route('/insert_client', methods=['POST'])
def insert_client():
    name = request.form['Name']
    return redirect('/signup')

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
