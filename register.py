import cs304dbi as dbi


def register_user(conn, full_name, wellesley_email, password, date):
    """Registers a new user in the database."""
    curs = dbi.dict_cursor(conn)
    
    curs.execute("""
        INSERT INTO user (name, user_email, password, join_date)
        VALUES (%s, %s, %s, %s);
    """, [full_name, wellesley_email, password, date])

    conn.commit()

    return True  # successfully registered

def check_user_exists(conn, wellesley_email):
    """Checks if a user with the given Wellesley College email exists in the database."""
    curs = dbi.dict_cursor(conn)
    # query = "SELECT * FROM users WHERE wellesley_email = %s", [wellesley_email]
    curs.execute('''SELECT * from user where user_email=%s ''', [wellesley_email])
    result = curs.fetchall()
    # result = dbi.query(conn, query, (wellesley_email,), result_set=True)
    
    # If the result set is not empty, the user exists
    return len(result) > 0
