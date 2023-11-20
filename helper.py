## some helper functions
import cs304dbi as dbi

def display_posts(conn):
    """
    returns a list of all active posts as dictionaries
    """
    curs = dbi.dict_cursor(conn)
    curs.execute("""
        select `user_email`, `description`, date(`post_date`) as 'post_date', 
        date(`expiration_date`) as 'expiration', `location`, `building`, `allergens`
        from post;
    """)
    posts = curs.fetchall()
    return posts


if __name__ == '__main__':
    db_to_use = 'wffa_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    conn = dbi.connect()
    print(display_posts(conn))