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
import profile
import register
import bcrypt
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
    ratings = helper.find_guide_ratings(conn)
    ## create time since posted tags
    for post in all_posts:
        if 'post_date' in post:
            #date_posted = datetime.strptime(post['post_date'], '%y-%m-%d %H:%M:%S')
            post['age'] = helper.find_post_age(post['post_date'])
        else:
            post['age'] = ''
    ## TO-DO: Implement function to remove expired posts from the database
    # customize page based on login status
    if not session.get('logged_in', False): # if not logged in
        session['logged_in'] = False
    print('**********************************')
    for key in session:
        print(key, session.get(key))
    return render_template('main.html',title='Free Food Alert', search_results=all_posts, ratedGuides=ratings, cookie=session)

@app.route('/rate-post/', methods=['GET', 'POST'])
def rate_post():
    """
    handle rating posts
    TO-DO: make this into Ajax embedded in homepage
    """
    if request.method == 'POST':
        data=request.form
        dbi.conf('wffa_db')
        conn = dbi.connect()
        helper.insert_rating(conn, data)
        flash(f"You rated {data.get('guide')}'s post {data.get('stars')} out of 5 stars")
        return redirect(url_for('index'))
    else: # request.method == 'GET':
        return redirect(url_for('index'))

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
        return render_template('search_results.html', title='Matching Food Posts', data=data)
    return render_template('search_form.html', title='Filter Food Posts', cookie=session, locations=locations, possible_allergens=possible_allergens)


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
        return redirect(url_for('index'))

    # Render the form template for GET requests
    return render_template('new_post_form.html', title='Insert New Food Posting', cookie=session)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        full_wellesley_email = request.form['wellesley_email']
        wellesley_email = full_wellesley_email.split('@')[0]
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        terms_checkbox = request.form.get('terms_checkbox')
        full_name = request.form['full_name']
        date = request.form['date']

        #deal with password encrypting
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        stored = hashed.decode('utf-8')


        # Check if the password and confirm_password match
        if password != confirm_password:
            return render_template('register_form.html', title='Register as a User', cookie=session, error='Passwords do not match')

        # Check if the terms and conditions checkbox is checked
        if not terms_checkbox:
            return render_template('register_form.html', title='Register as a User', cookie=session, error='Please agree to the terms and conditions')
        
        conn=dbi.connect()
        result = register.register_user(conn, full_name, wellesley_email, hashed, date)
        if result:
            # Redirect to a success page or (currently) login page
            return redirect(url_for('index'))
        else:
            return render_template('register_form.html', title='Register as a User', cookie=session, error='Registration failed. Please try again.')

    else:
        # Render the registration form for GET requests
        return render_template('register_form.html', title='Register as a User', cookie=session, error=None)

"""
Lets users become food guides (ie, food guide column for user becomes a 1)
"""
@app.route('/become_food_guide', methods=['POST'])
def become_food_guide():
    # Get the user's email from the session
    user_email = session.get('user_email')

    if not user_email:
        #user isn't logged in
        return redirect(url_for('login'))  # Redirect to login page

    # Update the user's food_guide status in the database
    conn = dbi.connect()
    profile.update_food_guide_status(conn, user_email)

    return redirect(url_for('user_profile'))


@app.route('/user_profile')
def user_profile():
    #get user email from session
    user_email = session.get('username')

    if not user_email: #not logged in
        return redirect(url_for('login'))

    # Get user data from the database (replace with your logic)
    conn = dbi.connect()
    user_data = profile.get_user_info(conn, user_email)

    if not user_data:
        return "User not found."

    return render_template('profile.html', title='View Profile', cookie=session, user=user_data)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['user_email']
        password = request.form['password']

        # Validate user 
        conn = dbi.connect()
        user_info = profile.validate_user(conn, user_email, password)
        if user_info: # the user exists
            # Set user_email in the session
            # session['user_email'] = user_email
            stored = user_info['password']
            hashed2 = bcrypt.hashpw(password.encode('utf-8'),
                            stored.encode('utf-8'))
            hashed2_str = hashed2.decode('utf-8')
            if hashed2_str == stored:
                flash('successfully logged in as '+ user_email)
                session['username'] = user_email
                session['uid'] = user_info['user_email']
                session['logged_in'] = True
                session['visits'] = 1
                # Redirect to the user profile page
                return redirect( url_for('user_profile') )
            else:
                flash('login incorrect. Try again or join') #  incorrect password
                return redirect(url_for('index'))

        else: # incorrect username
            flash('login incorrect. Try again or join')
            return redirect(url_for('index'))
    else:
        # Render the login form for GET requests
        print("***************recieved GET login request")
        return render_template('login.html', title='Log Into Free Food Alert', cookie=session)

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
