import cs304dbi as dbi

def insert_post(conn, user_email, description, post_date, expiration_date, location, building, allergens):
    curs = dbi.dict_cursor(conn)
   

    curs.execute('''insert into post(user_email, description, post_date, expiration_date, location, building, allergens)
                    values(%s, %s, %s, %s, %s, %s, %s)''',
                    [user_email, description, post_date, expiration_date, location, building, ','.join(allergens)])
    conn.commit()
