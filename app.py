from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from apscheduler.schedulers.background import BackgroundScheduler
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
import information
from datetime import datetime, timedelta

# Initialize the scheduler for deleting the expired post
scheduler = BackgroundScheduler()

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
        # check if they are rating themselves
        if data.get('guide') == data.get('user'):
            flash(f"You can not rate yourself")
            return redirect(url_for('index'))
        else:
            helper.insert_rating(conn, data)
            flash(f"You rated {data.get('guide')}'s post {data.get('stars')} out of 5 stars")
            return redirect(url_for('index'))
    else: # request.method == 'GET':
        # go back
        return redirect(url_for('index'))

@app.route('/search/', methods = ['GET', 'POST'])
def search_posts():
    '''
    Handles searching of posts based on specified search criteria
    '''
    conn = dbi.connect()
    locations = information.locations
    if not session.get('logged_in', False): # if not logged in
        session['logged_in'] = False
    possible_allergens = information.possible_allergens

    if request.method == 'POST':
        location = request.form.getlist('location')
        allergens = request.form.getlist('allergens')
        date_posted = request.form['date_posted']

        search_information = {'location': location, 
                                'allergens': allergens,
                                'date_posted': date_posted}
        data = search.search_for_post(conn, search_information)
        print('data:')
        print(data)
        return render_template('search_results.html', title='Matching Food Posts', cookie=session, data=data)
    return render_template('search_form.html', title='Filter Food Posts', cookie=session, locations=locations, possible_allergens=possible_allergens)


@app.route('/insert', methods=['GET', 'POST'])
def new_post():
    '''
    Create a new post with given information
    '''
    if not session.get('logged_in', False): # if not logged in
        session['logged_in'] = False
        flash("You must be logged in to access this page")
        return redirect(url_for('user_profile'))
    conn = dbi.connect()
    user_email = session.get('username')
    user_information = profile.get_user_info(conn, user_email)
    food_guide_status = user_information['food_guide']

    if food_guide_status != 1:
        flash("Please become a food guide ")
        return redirect(url_for('user_profile'))

    if request.method == 'POST':
        conn = dbi.connect()

        # Retrieve form data
        full_user_email = request.form['user_email']
        user_email = full_user_email.split('@')[0]
        food_name = request.form['food_name']
        food_description = request.form['food_description']
        allergens = request.form.getlist('allergens')
        print("will allergens print?")
        print(''.join(allergens))
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

        insert.update_user_post_count(conn, user_email)

        # Redirect to a success page or any other page
        return redirect(url_for('index'))

    # Render the form template for GET requests
    return render_template('new_post_form.html', title='Insert New Food Posting', cookie=session, possible_allergens=information.possible_allergens)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    '''
    Register a new user and update the database
    '''
    conn=dbi.connect()
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
            flash('Passwords do not match')
            return render_template('register_form.html', title='Register as a User', cookie=session, error='Passwords do not match')

        # Check if the terms and conditions checkbox is checked
        if not terms_checkbox:
            flash('Please agree to the terms and conditions')
            return render_template('register_form.html', title='Register as a User', cookie=session, error='Please agree to the terms and conditions')
        
        # Check if user exists
        existing_user = register.check_user_exists(conn, wellesley_email)
        if existing_user:
            return render_template('register_form.html', title='Register as a User', cookie=session, error='User already exists. Please login.')
        
        result = register.register_user(conn, full_name, wellesley_email, hashed, date)
        if result:
            # Redirect to a success page or (currently) login page
            flash(f"Registered user {wellesley_email}")
            session['username'] = wellesley_email
            session['uid'] = wellesley_email
            session['logged_in'] = True
            session['visits'] = 1
            return redirect(url_for('index'))
        else:
            flash("Registration failed. Please try again.")
            return render_template('register_form.html', title='Register as a User', cookie=session, error='Registration failed. Please try again.') # where should this show?

    else:
        # Render the registration form for GET requests
        return render_template('register_form.html', title='Register as a User', cookie=session, error=None)

"""
Lets users become food guides (ie, food guide column for user becomes a 1)
"""
@app.route('/become_food_guide', methods=['POST'])
def become_food_guide():
    '''
    Allow a user to become a food guide and make posts.
    '''
    # Get the user's email from the session
    user_email = session.get('username')
    print(user_email)
    if not user_email:
        #user isn't logged in
        return redirect(url_for('login'))  # Redirect to login page

    # Update the user's food_guide status in the database
    conn = dbi.connect()
    profile.update_food_guide_status(conn, user_email)

    return redirect(url_for('user_profile'))


@app.route('/user_profile')
def user_profile():
    '''
    Gets user information for a profile page
    '''
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
    '''
    Allows users to login to the website.
    '''
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

@app.route('/logout')
def logout():
    session.clear()  # Clear all session variables
    flash('You have been logged out.')
    return redirect(url_for('index'))

# Remove expired posts every 24 hours
@scheduler.scheduled_job('interval', hours=24)
def remove_expired_posts_job():
    conn = dbi.connect()
    helper.remove_expired_posts(conn)
    print('Expired posts have been removed.')

# Start the scheduler
scheduler.start()

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
