from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
# import cs304dbi_sqlite3 as dbi

import random
import search
import helper
import insert
from datetime import datetime, timedelta

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    conn = dbi.connect()
    all_posts = helper.display_posts(conn)
    ## TO-DO: Implement function to remove expired posts from the database
    return render_template('main.html',title='Free Food Alert', search_results=all_posts, now = datetime.date(datetime.now()))

@app.route('/search/', methods = ['GET', 'POST'])
def search_posts():
    conn = dbi.connect()
    locations=['Acorns', 'Alumnae Hall', 'Athletic Maintenance Facility', 'Bates Hall', 
    'Beebe Hall', 'Billings', 'Boathouse', 'Campus Police Headquarters', 'Cazenove Hall', 
    'Cedar Lodge', 'Cervantes', 'Cheever House', 'Child Study Center', 'Claflin Hall', 
    'Collins Cinema', 'Continuing Education Office', 'Davis Hall', 'Davis Museum', 
    'Davis Parking Facility', 'Day Care Center', 'Distribution Center', 'Dower House', 
    'East Lodge', 'Fiske House', 'Founders Hall', 'Freeman Hall', 'French House - Carriage', 
    'French House - Main', 'Golf House', 'Green Hall', 'Grounds', 'Hallowell House', 'Harambee House', 
    'Hemlock', 'Homestead', 'Horton House', 'Instead', 'Jewett Art Center', 'Keohane Sports Center', 
    'Lake House', 'Library', 'Lulu Chow Wang Campus Center', 'Margaret Ferguson Greenhouses', 
    'McAfee Hall', 'Motor Pool', 'Munger Hall', 'Nehoiden House', 'Observatory', 'Orchard Apts', 
    'Pendleton Hall East', 'Pendleton Hall West', 'Physical Plant', 'Pomeroy Hall', 
    "President's House", 'Ridgeway Apts', 'Schneider Center', 'Science Center', 'Service Building', 
    'Severance Hall', 'Shafer Hall', 'Shakespeare', 'Shepard House', 'Simpson Hall', 'Simpson West', 
    'Slater International Center', 'Stone Center', 'Stone Hall', 'Tower Court East', 'Tower Court West',
     'Trade Shops Building', 'Tau Zeta Epsilon', 'Waban House', 'Weaver House', 'Webber Cottage', 
     'Wellesley College Club', 'West Lodge', 'Whitin House', 'Zeta Alpha House']

    possible_allergens = ['Soy', 'Peanuts', 'Dairy', 'Eggs', 'Shellfish', 'Nuts', 'Sesame', 'Gluten']
    if request.method == 'POST':
        location = request.form.getlist('location')
        allergens = request.form.getlist('allergens')
        date_posted = request.form['date_posted']

        search_information = {'location': location, 
                                'allergens': allergens,
                                'date_posted': date_posted}
        data = search.search_for_post(conn, search_information)
        return render_template('search_results.html', data=data)
    return render_template('search_form.html', locations=locations, possible_allergens=possible_allergens)

# @app.route('/new_post', methods=['POST'])
# def new_post():
#     if request.method == 'POST':
#         conn = dbi.connect()

#         # Retrieve form data
#         user_email = request.form['user_email']
#         food_name = request.form['food_name']
#         food_description = request.form['food_description']
#         allergens = request.form.getlist('allergens')
#         expiration_date = request.form['expiration_date']
#         building = request.form['building_dropdown']
#         room_number = request.form['room_number']
#         # Handle optional image upload
#         food_image = request.files['food_image'] if 'food_image' in request.files else None

#         #insert into database
#         post_date = datetime.date(datetime.now())
#         insert.insert_post(conn, user_email, food_name, food_description, post_date, allergens, expiration_date, building, room_number)
#         all_posts = helper.display_posts(conn)

#         # Redirect to a success page or any other page
#         return render_template('main.html',title='Free Food Alert', search_results=all_posts, now = datetime.date(datetime.now()))
#     # Render the form template for GET requests
#     return render_template('main.html',title='Free Food Alert', search_results=all_posts, now = datetime.date(datetime.now()))

@app.route('/insert', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        conn = dbi.connect()

        # Retrieve form data
        full_user_email = request.form['user_email']
        user_email = full_user_email.split('@')[0]
        food_name = request.form['food_name']
        food_description = request.form['food_description']
        allergens = request.form.getlist('allergens')
        expiration_date = request.form['expiration_date']
        building = request.form['building_dropdown']
        room_number = request.form['room_number']
        # Handle optional image upload
        food_image = request.files['food_image'] if 'food_image' in request.files else None

        # Insert into the database
        post_date = datetime.date(datetime.now())
        insert.insert_post(conn, user_email, food_description, post_date, expiration_date, room_number, building, allergens)
        # insert.insert_post(conn, user_email, food_name, food_description, post_date, allergens, expiration_date, building, room_number)
        all_posts = helper.display_posts(conn)

        # Redirect to a success page or any other page
        return render_template('main.html', title='Free Food Alert', search_results=all_posts, now=datetime.date(datetime.now()))

    # Render the form template for GET requests
    return render_template('new_post_form.html', title='Free Food Alert')

@app.route('/register', methods=['GET', 'POST'])
def registration():
    return render_template('register_form.html')

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'wffa_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    app.debug = True
    app.run('0.0.0.0',port)
