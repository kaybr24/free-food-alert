import cs304dbi as dbi
from flask import flash

def insert_post(conn, post_date, information):
    """
    Insert a new food post into the database, given post information. 
    Returns the new post_id
    """
    curs = dbi.dict_cursor(conn)
    full_user_email = information['user_email']
    user_email = full_user_email.split('@')[0]
    food_description = information['food_description']
    allergens = information.getlist('allergens')
    
    expiration_date = information['expiration_date']
    building = information['building_dropdown']
    room_number = information['room_number']

    # check if room number is an acceptable length
    if len(room_number) > 30:
        flash("Room numbers must be less than 30 characters long")
        room_number = room_number[:30]            

    curs.execute('''insert into post(user_email, description, post_date, expiration_date, location, building, allergens)
                    values(%s, %s, %s, %s, %s, %s, %s)''',
                    [user_email, food_description, post_date, expiration_date, room_number, building, ','.join(allergens)])
    conn.commit()

    curs.execute('''select last_insert_id()''')
    return curs.fetchone().get('last_insert_id()')

def get_active_user_post_count(conn, user_email):
    """
    Finds count of active posts made by user
    """
    curs = conn.cursor()
    query = "SELECT COUNT(post_id) FROM post WHERE user_email=%s"
    curs.execute(query, [user_email])
    numPosts = curs.fetchone()[0]
    return numPosts

def update_user_historical_post_count(conn, user_email):
    """
    Updates the count of historical posts made by user
    """
    curs = conn.cursor()
    query = "UPDATE user SET post_count = post_count + 1 where user_email = %s"
    curs.execute(query, (user_email))
    conn.commit()

def insert_image(conn, user_email, post_id, filetype):
    """
    insert the user_email, post_id, and a unique image id into picture table
    """
    # insert new image row
    curs = conn.cursor()
    query = """
        INSERT INTO `picture`(user_email, post_id, filetype)
        VALUES (%s, %s, %s);
    """
    curs.execute(query, [user_email, post_id, filetype])
    conn.commit()
    # find the image id
    curs.execute("""
        SELECT last_insert_id()
    """)
    return curs.fetchone()