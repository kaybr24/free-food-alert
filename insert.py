import cs304dbi as dbi

def insert_post(conn, user_email, description, post_date, expiration_date, location, building, allergens):
    curs = dbi.dict_cursor(conn)
   

    curs.execute('''insert into post(user_email, description, post_date, expiration_date, location, building, allergens)
                    values(%s, %s, %s, %s, %s, %s, %s)''',
                    [user_email, description, post_date, expiration_date, location, building, ','.join(allergens)])
    conn.commit()

def update_user_post_count(conn, user_email):
    curs = conn.cursor()
    query = "SELECT COUNT(*) FROM post WHERE user_email=%s"
    curs.execute(query, (user_email,))
    posts = curs.fetchone()[0]

    update_post_count = "UPDATE user SET post_count = %s where user_email = %s"
    curs.execute(update_post_count, (posts, user_email))

    conn.commit()