import cs304dbi as dbi

def update_food_guide_status(conn, user_email):
    curs = dbi.dict_cursor(conn)
    # Update the user's food_guide status to 1
    curs.execute("UPDATE user SET food_guide = 1 WHERE user_email = %s", [user_email])
    conn.commit()
    conn.close()

def get_user_info(conn, user_email):
    curs = dbi.dict_cursor(conn)
    curs.execute("SELECT * FROM user WHERE user_email = %s", [user_email])
    user_data = curs.fetchone()
    conn.close()
    return user_data

def validate_user(conn, user_email, password):
    curs = dbi.dict_cursor(conn)
    curs.execute('''SELECT user_email, password
                    from user where user_email = %s''', [user_email])
    user = curs.fetchone()
    conn.close()
    return user