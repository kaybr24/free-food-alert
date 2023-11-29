import cs304dbi as dbi


def register_user(conn, full_name, wellesley_email, password, date):
    curs = dbi.dict_cursor(conn)
    
    curs.execute("""
        INSERT INTO user (name, user_email, password, join_date)
        VALUES (%s, %s, %s, %s);
    """, [full_name, wellesley_email, password, date])

    conn.commit()

    return True  # successfully registered