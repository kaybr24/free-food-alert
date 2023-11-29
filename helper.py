## some helper functions
import cs304dbi as dbi
from datetime import datetime, timedelta

def display_posts(conn):
    """
    returns a list of all active posts as dictionaries
    """
    curs = dbi.dict_cursor(conn)
    curs.execute("""
        select `user_email`, `description`, `post_date`, 
        date(`expiration_date`) as 'expiration', `location`, `building`, `allergens`
        from post;
    """)
    posts = curs.fetchall()
    return posts

def find_guide_ratings(conn, specific_guide=None):
    curs = dbi.dict_cursor(conn)
    if specific_guide:
        curs.execute("""select avg(rating) from rating where guide_email like %s;""",
            [specific_guide])
        rating = curs.fetchone()
    else:
        curs.execute("""select avg(rating), guide_email 
            from rating 
            group by guide_email;
            """)
        rating = curs.fetchall()
    return rating

def find_post_age(post_date):
    """given the age of a post, return a number, string pair
    representing the age and time units of the post"""
    today = datetime.now()
    delta = today - post_date
    if delta.days > 7:
        if delta.days//7 == 1:
            return ('1 week')
        else:
            return (str(delta.days//7) +' weeks')
    elif delta.days > 0:
        if delta.days == 1:
            return ("1 day")
        else:
            return (str(delta.days) + ' days')
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


if __name__ == '__main__':
    db_to_use = 'wffa_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    conn = dbi.connect()
    # testing find_post_age()
    time = datetime(2023, 10, 23)
    print(find_post_age(time))
    #print(display_posts(conn))