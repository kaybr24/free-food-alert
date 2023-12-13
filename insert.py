import cs304dbi as dbi

def insert_post(conn, post_date, information):
    curs = dbi.dict_cursor(conn)
    full_user_email = information['user_email']
    user_email = full_user_email.split('@')[0]
    # food_name = information['food_name']
    food_description = information['food_description']
    allergens = information.getlist('allergens')
    
    expiration_date = information['expiration_date']
    building = information['building_dropdown']
    room_number = information['room_number']


    curs.execute('''insert into post(user_email, description, post_date, expiration_date, location, building, allergens)
                    values(%s, %s, %s, %s, %s, %s, %s)''',
                    [user_email, food_description, post_date, expiration_date, room_number, building, ','.join(allergens)])
    conn.commit()

    curs.execute('''select last_insert_id()''')
    return curs.fetchone().get('last_insert_id()')

def update_user_post_count(conn, user_email):
    curs = conn.cursor()
    query = "SELECT COUNT(*) FROM post WHERE user_email=%s"
    curs.execute(query, (user_email,))
    posts = curs.fetchone()[0]

    update_post_count = "UPDATE user SET post_count = %s where user_email = %s"
    curs.execute(update_post_count, (posts, user_email))

    conn.commit()

def insert_image(conn, user_email, post_id, filetype):
    """
    insert the user_email, post_id, and a unique image id into picture
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