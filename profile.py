import cs304dbi as dbi

def update_food_guide_status(conn, user_email):
    curs = dbi.dict_cursor(conn)
    # Update the user's food_guide status to 1
    curs.execute("UPDATE user SET food_guide = 1 WHERE user_email = %s", [user_email])
    conn.commit()

def get_user_info(conn, user_email):
    curs = dbi.dict_cursor(conn)
    curs.execute("SELECT * FROM user WHERE user_email = %s", [user_email])
    user_data = curs.fetchone()
    return user_data

def validate_user(conn, user_email, password):
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT user_email, password
                    from user where user_email = %s''', [user_email])
    user = curs.fetchone()
    return user

def get_all_posts(conn, user_email):
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT `post_id`, `user_email`, `description`, `post_date`, 
        date(`expiration_date`) as 'expiration', `location`, `building`, `allergens`
        from post where user_email = %s order by 'post_date' desc''', [user_email])
    user_posts = curs.fetchall()
    return user_posts
