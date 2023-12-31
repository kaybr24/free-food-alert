from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
# from apscheduler.schedulers.background import BackgroundScheduler
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
# scheduler = BackgroundScheduler()

# File upload handling
# I am using the static folder because there are no private images that shouldn't be viewed by everyone
UPLOAD_FOLDER = 'static/uploads/' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # 3 MB

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
    # helper.remove_expired_posts(conn)
    all_posts = helper.display_posts(conn)
    ratings = helper.find_guide_ratings(conn)

    comments = {}
    pictures = {}
    for post in all_posts:
        post_id = post.get('post_id')
        if post_id:
            post_comments = helper.get_comments_for_post(conn, post_id)
            comments[post_id] = post_comments
            
            # if there is an image to be found
            picIDs = helper.get_images_for_post(conn, post_id)
            if picIDs:
                for image in picIDs:
                    file = helper.construct_file_name(image, app.config['UPLOAD_FOLDER'])
                    pictures[post_id] = file 

    ## create time since posted tags
    for post in all_posts:
        if 'post_date' in post:
            post['age'] = helper.find_post_age(post['post_date'])
        else:
            post['age'] = ''

    # customize page based on login status
    if not session.get('logged_in', False): # if not logged in
        session['logged_in'] = False # for easier comparisons in base.html
    
    # customize page based on which posts were rated by this user
    uid = session.get("uid", False)
    if uid: # if logged in
        conn = dbi.connect()
        rated_posts = helper.select_user_ratings(conn, uid)
    else:
        rated_posts = {}

    return render_template('main.html',title='Free Food Alert', comments=comments, search_results=all_posts, 
                            ratedGuides=ratings, cookie=session, img=pictures, rated=rated_posts)

@app.route('/rate-post/', methods=['GET', 'POST'])
def rate_post():
    """
    handle rating posts
    """
    if request.method == 'GET':
        # go back
        return redirect(url_for('index'))
    else: # request.method == 'POST':
        data = request.form
        conn = dbi.connect()
        # check if they are rating themselves
        if data.get('guide') == data.get('user'):
            flash(f"You can not rate yourself")
            return redirect(url_for('index'))
        else:
            rate_msg = helper.insert_rating(conn, data)
            flash(rate_msg)
            return redirect(url_for('index'))

@app.route('/search/', methods = ['GET'])
def search_posts():
    '''
    Handles searching of posts based on specified search criteria
    '''
    # if not logged in, for custom display in base.html
    if not session.get('logged_in', False): 
        session['logged_in'] = False

    # retireve information on valid search results
    possible_allergens = information.possible_allergens
    locations = information.locations

    # user has not searched anything yet
    if not request.args: 
        return render_template('search_form.html', title='Filter Food Posts', cookie=session, 
                                locations=locations, possible_allergens=possible_allergens)
    # user wants to see search results
    else: 
        building = request.args.getlist('building')
        allergens = request.args.getlist('allergens')
        date_posted = request.args['date_posted']

        search_information = {'building': building, 
                                'allergens': allergens,
                                'date_posted': date_posted}
        conn = dbi.connect()
        data = search.search_for_post(conn, search_information)
        return render_template('search_results.html', title='Matching Food Posts', cookie=session, data=data)
    

@app.route('/insert/', methods=['GET', 'POST'])
def new_post():
    '''
    Create a new post with given information
    '''
    if not session.get('logged_in', False): # if not logged in
        session['logged_in'] = False # for easier comparison in base.html
        flash("You must be logged in to access this page")
        return redirect(url_for('user_profile'))
    conn = dbi.connect()
    user_email = session.get('username')
    user_information = profile.get_user_info(conn, user_email)
    food_guide_status = user_information['food_guide']

    if food_guide_status != 1:
        flash("Please become a food guide ")
        return redirect(url_for('user_profile'))

    if request.method == 'GET':
        # Render the form template for GET requests
        return render_template('new_post_form.html', title='Insert New Food Posting', cookie=session, 
                                possible_allergens=information.possible_allergens)

    elif request.method == 'POST':

        # Insert into the database
        post_date = datetime.now()
        conn = dbi.connect()
        post_id = insert.insert_post(conn, post_date, request.form)

        # increment historical post count by 1
        insert.update_user_historical_post_count(conn, user_email)

        # Handle optional image upload - assume there is only one image
        file = request.files['food_image'] if 'food_image' in request.files else None
        if file and file.filename == "":
            flash("No file selected")
        if file and helper.allowed_file(file.filename): # if there was a file and it has a legal name
            # insert image name into picture table
            conn2 = dbi.connect()
            filetype = file.filename.split('.')[-1]
            image_id = insert.insert_image(conn2, user_email, post_id, filetype)

            # save image to uploads file
            filename = secure_filename(str(post_id) + "_" + str(image_id) + "." + filetype)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("You inserted a post with an image")
        
        # Redirect to a success page or any other page
        return redirect(url_for('index'))

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    '''
    Register a new user and update the database
    '''
    if request.method == 'GET':
        # Render the registration form for GET requests
        return render_template('register_form.html', title='Register as a User', cookie=session, error=None)
    else: # if request.method == 'POST':
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
        conn1=dbi.connect()
        existing_user = register.check_user_exists(conn1, wellesley_email)
        if existing_user:
            flash('User already exists. Please login.')
            return render_template('register_form.html', title='Register as a User', cookie=session, error='User already exists. Please login.')
        
        conn2=dbi.connect()
        result = register.register_user(conn2, full_name, wellesley_email, hashed, date)
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
        


@app.route('/become_food_guide/', methods=['POST'])
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


@app.route('/user_profile/')
def user_profile():
    '''
    Gets user information for a profile page
    '''
    #get user email from session
    user_email = session.get('username')

    if not user_email: #not logged in
        return redirect(url_for('login'))

    # Get user data from the database
    conn = dbi.connect()
    user_data = profile.get_user_info(conn, user_email)
    # active post count
    active_post_count = insert.get_active_user_post_count(conn, user_email)
    user_data["active_posts"] = active_post_count
    # historical post count
    if not user_data.get("post_count", False):
        user_data["post_count"] = 0
    all_posts = profile.get_all_posts(conn, user_email)
    ratings = helper.find_guide_ratings(conn)

    comments = {}
    pictures = {}
    for post in all_posts:
        post_id = post.get('post_id')
        if post_id:
            post_comments = helper.get_comments_for_post(conn, post_id)
            comments[post_id] = post_comments
            # if there is an image to be found
            picIDs = helper.get_images_for_post(conn, post_id)
            if picIDs:
                for image in picIDs:
                    file = helper.construct_file_name(image, app.config['UPLOAD_FOLDER'])
                    pictures[post_id] = file

    ## create time since posted tags
    for post in all_posts:
        if 'post_date' in post:
            #date_posted = datetime.strptime(post['post_date'], '%y-%m-%d %H:%M:%S')
            post['age'] = helper.find_post_age(post['post_date'])
        else:
            post['age'] = ''

    # customize page based on login status
    if not session.get('logged_in', False): # if not logged in
        session['logged_in'] = False    

    if not user_data:
        return "User not found."

    return render_template('profile.html', title='View Profile', cookie=session, user=user_data, posts=all_posts, 
                            comments=comments, ratedGuides=ratings, img=pictures)



@app.route('/login/', methods=['GET', 'POST'])
def login():
    '''
    Allows users to login to the website.
    '''
    if request.method == 'GET':
        # Render the login form for GET requests
        return render_template('login.html', title='Log Into Free Food Alert', cookie=session)

    if request.method == 'POST':
        user_email = request.form['user_email']
        password = request.form['password']

        # Validate user 
        conn = dbi.connect()
        user_info = profile.validate_user(conn, user_email, password)
        if user_info: # the user exists
            # Set user_email in the session
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
                return redirect(url_for('login'))

        else: # incorrect username
            flash('login incorrect. Try again or join')
            return redirect(url_for('index'))
    

@app.route('/add_comment/', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        data = request.form
        post_id = data.get('post_id')
        user_email = session.get('username')
        comment_text = data.get('comment_text')

        if not post_id:
            flash("unable to comment")
            return redirect(url_for('index'))
        if not comment_text:
            flash('please provide comment text')
            return redirect(url_for('index'))
       
        # Insert the comment into the database
        conn = dbi.connect()
        helper.insert_comment(conn, post_id, user_email, comment_text)
        
        flash('Comment added successfully.')
        return redirect(url_for('index'))

@app.route('/remove-post/', methods=['POST'])
def remove_post():
    """
    permantly delete the given post
    """
    # confirm they are logged in
    user_email = session.get('uid', False)
    if not user_email:
        flash("You must be logged in to delete a post")
        return redirect(url_for('login'))

    # confirm that this belongs to the user
    post_id = request.form.get("post_id")
    conn = dbi.connect()
    post_data = helper.get_post_info(conn, post_id)
    if user_email != post_data.get("user_email"):
        flash(f"You can not delete another Food Guide's post")
        return redirect(url_for('index'))

    # Delete post
    helper.remove_post(conn, post_id, app.config["UPLOAD_FOLDER"])
    desc = post_data.get("description")
    day = post_data.get("post_date")
    flash(f"Successfully deleted post {desc} from {day}")
    return redirect(url_for('user_profile'))
    

@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    """
    Allow user to edit values in the given post
    """
    # confirm they are logged in
    user_email = session.get('uid', False)
    if not user_email:
        flash("You must be logged in to edit a post")
        return redirect(url_for('login'))

    # Get the post data based on post_id
    conn = dbi.connect()
    post_data = helper.get_post_info(conn, post_id)
    post_data['allergens'] = post_data.get('allergens', '').title().split(',')

    # confirm that this post exists and belongs to the user
    if not post_data:
        flash(f"Post {post_id} not found.")
        return redirect(url_for('user_profile'))
    elif user_email != post_data.get("user_email"):
        flash(f"You can not edit another Food Guide's post")

    # retrieve existing image, if any
    conn = dbi.connect()
    image = helper.get_images_for_post(conn, post_id)
    if image: # exists
        # only use one image
        image = image[0]
        imageName = helper.construct_file_name(image, app.config['UPLOAD_FOLDER'])
        post_data['image_url'] = imageName

    # render template with existing data
    if request.method == 'GET':
        return render_template('edit_post.html', title='Edit Post', post=post_data, cookie=session, 
                possible_allergens=information.possible_allergens, locations=information.locations)

    elif request.method == 'POST':
        # Update the post with the new data
        updated_description = request.form['food_description']
        updated_allergens = request.form.getlist('allergens')  
        updated_expiration_date = request.form['expiration_date']
        updated_building = request.form['building']
        updated_room_number = request.form['room_number']

        # Update the post contents
        conn2 = dbi.connect() # could this fix the "lock timeout exceeded"?
        helper.update_post(
            conn2,
            post_id,
            updated_description,
            updated_allergens,
            updated_expiration_date,
            updated_building,
            updated_room_number,
        )  

        # Update the image, if any
        new_image = request.files['food_image'] if 'food_image' in request.files else None
        if new_image and new_image.filename == "": # empty upload
            flash("No file selected")
        if new_image and helper.allowed_file(new_image.filename): # file type is legal
            Fname = helper.replace_image(conn, user_email, post_id, new_image, app.config['UPLOAD_FOLDER'])
            if Fname:
                flash(f"You updated the image for your post: {updated_description[:20]}...")
        return redirect(url_for('user_profile'))


@app.route('/logout')
def logout():
    session.clear()  # Clear all session variables
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/picfile')
def picfile():
    session.clear()  # Clear all session variables
    flash('You have been logged out.')
    return redirect(url_for('index'))

# # Remove expired posts every 24 hours
# @scheduler.scheduled_job('interval', hours=24)
# def remove_expired_posts_job():
#     conn = dbi.connect()
#     helper.remove_expired_posts(conn)
#     print('Expired posts have been removed.')

# Start the scheduler
# scheduler.start()

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # Check if the user is logged in
    if not session.get('logged_in', False):
        abort(401)  # Unauthorized

    # Get the user's email from the session
    user_email = session.get('username')

    # Check if the user is the one who posted the specified post_id
    conn = dbi.connect()
    post_data = helper.get_post_info(conn, post_id)
    
    if not post_data or post_data['user_email'] != user_email:
        abort(403)  # Forbidden

    # Delete the post and associated comments and images
    helper.remove_post(conn, post_id, app.config['UPLOAD_FOLDER'])

    flash(f"Post {post_id} has been deleted.")
    return redirect(url_for('index'))

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
