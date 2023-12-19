## some helper functions
import cs304dbi as dbi
from datetime import datetime, timedelta
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def display_posts(conn):
    """
    returns a list of all active posts as dictionaries
    """
    curs = dbi.dict_cursor(conn)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    query = """
        SELECT  `post_id`, `user_email`, `description`, `post_date`, 
        date(`expiration_date`) as 'expiration', `location`, `building`, `allergens`
        FROM post
        WHERE expiration_date >= %s
        order by `post_date` desc;
    """
    
    curs.execute(query, (current_date,))
    posts = curs.fetchall()


    # curs.execute("""
    #     select `post_id`, `user_email`, `description`, `post_date`, 
    #     date(`expiration_date`) as 'expiration', `location`, `building`, `allergens`
    #     from post
    #     order by `post_date` desc;
    # """)
    # posts = curs.fetchall()
    return posts

def find_guide_ratings(conn, specific_guide=None):
    '''
    if no specific_guide is specified, returns a dictionary of [avgrating, count(ratings)] for each guide
    if a specific_guide is specified, returns a dictionary with one element (the rating, count pair for that guide)
    '''
    curs = dbi.dict_cursor(conn)
    rated_guides = {}
    if specific_guide:
        curs.execute("""select avg(rating), count(rating) from rating where guide_email like %s;""",
            [specific_guide])
        rating = curs.fetchone()
        rated_guides = {specific_guide: [float(rating.get('avg(rating)')), float(rating.get('count(rating)'))]}
    else:
        # atomic read should be thread-safe
        curs.execute("""select avg(rating), guide_email, count(rating)
            from rating 
            group by guide_email;
            """)
        rating = curs.fetchall()
        for guideDict in rating:
            guide = guideDict.get('guide_email')
            stars = guideDict.get('avg(rating)')
            count = guideDict.get('count(rating)')
            if stars:
                rated_guides[guide] = [float(stars), int(count)]
            # else:  
            #     rated_guides[guide] = [0, 0]
    return rated_guides

def insert_rating(conn, rating):
    """
    given the username, food guide and star rating as a dictionary, 
    insert the new rating into the database
    """
    curs = dbi.dict_cursor(conn)
    # atomic insert should be thread-safe
    query = """insert into rating(`post_id`, `guide_email`, `rater_email`, `rating`)
        values (%s, %s, %s, %s)
        on duplicate key update
        `rating` = %s;""" # change primary key so this works
    values = [
        rating.get('postID'), 
        rating.get('guide'),
        rating.get('user'),
        rating.get('stars'),
        rating.get('stars')
        ]
    result = curs.execute(query, values)
    conn.commit()
    # result is 1 if rating was inserted, and 2 if rating was updated
    # not sure why, but I noticed this output behaviour
    if result == 2:
        return f"You updated your rating of {rating.get('guide')}'s post to be {rating.get('stars')} out of 5 stars"
    else:
        return f"You rated {rating.get('guide')}'s post {rating.get('stars')} out of 5 stars"

def find_post_age(post_date):
    """given the age of a post, return a (number, string) pair
    representing the age and time units of the post"""
    today = datetime.now()
    delta = today - post_date
    dpm = 7*52.143/12 # days per month
    if delta.days > dpm:
        if delta.days//dpm == 1:
            return ('1 month')
        else:
            return (str(int(delta.days//dpm)) +' months')
    elif delta.days > 7:
        if delta.days//7 == 1:
            return ('1 week')
        else:
            return (str(delta.days//7) +' weeks')
    elif delta.days > 0:
        if delta.days == 1:
            return ("1 day")
        else:
            return (str(delta.days) + ' days')
    elif delta.seconds > 3600:
        if delta.seconds//3600 == 1:
            return('1 hour')
        else:
            print(today, post_date, delta.seconds/3600)
            return (str(delta.seconds//3600) + ' hours')
    elif delta.seconds > 60:
        if delta.seconds//60 == 1:
            return('1 minute')
        else:
            return (str(delta.seconds//60) + ' minutes')
    else:
        if delta.seconds == 1:
            return ('1 second')
        else:
            return (str(delta.seconds) + ' seconds')

def remove_expired_posts(conn):
    """
    Remove expired posts from the database.
    """
    curs = dbi.dict_cursor(conn)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        DELETE FROM post
        WHERE expiration_date < %s
    """
    #curs.execute("DELETE FROM rating WHERE post_id IN (SELECT post_id FROM post WHERE expiration_date < %s)", (current_date,))
    # atomic delete should be thread-safe
    curs.execute(query, [current_date])
    conn.commit()
    
def insert_comment(conn, post_id, user_email, comment):
    '''
    Inserts comment to a post into table
    '''
    curs = dbi.dict_cursor(conn)
    now = datetime.now()
    commentDate = now.strftime('%Y-%m-%d %H:%M:%S')
    # atomic insert should be thread-safe
    curs.execute('''insert into comments(post_id, user_email, comment, date)
                    values(%s, %s, %s, %s)''',
                    [post_id, user_email, comment, commentDate])

    # query = "INSERT INTO comments (post_id, user_email, comment, date) VALUES ((%s, %s, %s, %s)"
    # values=[post_id, user_email, comment, commentDate]
    # curs.execute(query, values)
    conn.commit()

def get_comments_for_post(conn, post_id):
    '''
    gets the comments for a post
    '''
    curs = dbi.dict_cursor(conn)
    # atomic read should be thread-safe
    query = "SELECT 'comment_id', 'post_id', 'user_email', 'comment', 'date' FROM comments WHERE post_id=%s ORDER BY date DESC"
    curs.execute(query, [post_id])
    return curs.fetchall()

def get_images_for_post(conn, post_id):
    '''
    gets the ids of picture(s) for a post
    '''
    curs = dbi.dict_cursor(conn)
    # atomic read should be thread-safe
    query = "SELECT image_id, filetype FROM picture WHERE post_id = %s"
    curs.execute(query, [post_id])
    return curs.fetchall()

def get_post_info(conn, post_id):
    '''
    gets all information for a post
    '''
    curs = dbi.dict_cursor(conn)
    query = "SELECT * from post WHERE post_id = %s"
    curs.execute(query, [post_id])
    return curs.fetchone()

def update_post(conn, post_id, updated_description, updated_allergens, updated_expiration_date, updated_building,updated_room_number):
    '''
    update the post of the user
    '''
    curs = conn.cursor()
    query = """
        UPDATE post
        SET description = %s,
            allergens = %s,
            expiration_date = %s,
            building = %s,
            location = %s
        WHERE post_id = %s
    """

    allergens_str = ",".join(updated_allergens)

   
    curs.execute(query, (updated_description, allergens_str, updated_expiration_date, updated_building, updated_room_number, post_id))

    conn.commit()

def remove_post(conn, post_id):
    """
    Remove a post and associated comments and images from the database.
    """
    curs = dbi.dict_cursor(conn)

    # Delete comments for the post
    curs.execute("DELETE FROM comments WHERE post_id = %s", [post_id])

    # Delete images for the post
    curs.execute("DELETE FROM picture WHERE post_id = %s", [post_id])

    # Delete the post
    curs.execute("DELETE FROM post WHERE post_id = %s", [post_id])

    conn.commit()


# def update_post_with_image(conn, post_id, description, allergens, expiration_date, building, room_number, filename):
#     curs = dbi.dict_cursor(conn)
#     query = """
#         UPDATE post
#         SET description=%s, allergens=%s, expiration_date=%s, building=%s, room_number=%s, image_filename=%s
#         WHERE post_id=%s
#     """
#     curs.execute(query, (description, allergens, expiration_date, building, room_number, filename, post_id))
#     conn.commit()

def update_post_with_image(conn, post_id, description, allergens, expiration_date, building, location, image_filename, user_email):
    '''
    Update a post with new information, and delete picture from table
    '''
    curs = dbi.dict_cursor(conn)
    allergens_str = ",".join(allergens)
    query = """
        UPDATE post
        SET description=%s, allergens=%s, expiration_date=%s, building=%s, location=%s
        WHERE post_id=%s
    """
    curs.execute(query, (description, allergens_str, expiration_date, building, location, post_id))
    
    # Delete the existing image associated with the post in the picture table
    delete_query = """
        DELETE FROM picture
        WHERE post_id = %s
    """
    curs.execute(delete_query, (post_id,))
    print("******************")
    print(post_id)
    conn.commit()
    
    # Insert the new image associated with the post
    insert_image_update(conn, post_id, description, allergens, expiration_date, building, location, image_filename, user_email)




def insert_image_update(conn, post_id, description, allergens, expiration_date, building, location, image_filename, user_email):
    '''
    Update the picture table with image
    '''
    curs = dbi.dict_cursor(conn)
    insert_query = """
        INSERT INTO picture (user_email, post_id, filetype)
        VALUES (%s, %s, %s)
    """
    if image_filename:
        parts = image_filename.split("_")
        curs.execute(insert_query, (user_email, post_id, 'jpg'))  # only using jpg for now
        conn.commit()
    

if __name__ == '__main__':
    db_to_use = 'wffa_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    conn = dbi.connect()
    # testing find_post_age()
    time = datetime(2023, 10, 23)
    print(find_post_age(time))
    # testing find_guide_ratings()
    print(find_guide_ratings(conn))
    print(find_guide_ratings(conn, 'kb102'))
    #print(display_posts(conn))
    print(get_image(conn, 3))