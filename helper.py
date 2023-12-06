## some helper functions
import cs304dbi as dbi
from datetime import datetime, timedelta

def display_posts(conn):
    """
    returns a list of all active posts as dictionaries
    """
    curs = dbi.dict_cursor(conn)
    curs.execute("""
        select `post_id`, `user_email`, `description`, `post_date`, 
        date(`expiration_date`) as 'expiration', `location`, `building`, `allergens`
        from post
        order by `post_date` desc;
    """)
    posts = curs.fetchall()
    return posts

def find_guide_ratings(conn, specific_guide=None):
    curs = dbi.dict_cursor(conn)
    rated_guides = {}
    if specific_guide:
        curs.execute("""select avg(rating), count(rating) from rating where guide_email like %s;""",
            [specific_guide])
        rating = curs.fetchone()
        rated_guides = {specific_guide: [float(rating.get('avg(rating)')), float(rating.get('count(rating)'))]}
    else:
        curs.execute("""select avg(rating), guide_email, count(rating)
            from rating 
            group by guide_email;
            """)
        rating = curs.fetchall()
        for guideDict in rating:
            guide = guideDict.get('guide_email')
            stars = guideDict.get('avg(rating)')
            count = guideDict.get('count(rating)')
            if stars:
                rated_guides[guide] = [float(stars), int(count)]
            else:  
                rated_guides[guide] = [0, 0]
    return rated_guides

def insert_rating(conn, rating):
    """
    given the username, food guide and star rating as a dictionary, 
    insert the new rating into the database
    """
    curs = dbi.dict_cursor(conn)
    query = """insert into rating(`post_id`, `guide_email`, `rater_email`, `rating`)
        values (%s, %s, %s, %s)
        on duplicate key update
        `rating` = %s;""" # change primary key so this works
    values = [
        rating.get('postID'), 
        rating.get('guide'),
        rating.get('user'),
        rating.get('stars'),
        rating.get('stars')
        ]
    curs.execute(query, values)
    conn.commit()

def find_post_age(post_date):
    """given the age of a post, return a number, string pair
    representing the age and time units of the post"""
    today = datetime.now()
    delta = today - post_date
    dpm = 7*52.143/12 # days per month
    if delta.days > dpm:
        if delta.days//dpm == 1:
            return ('1 month')
        else:
            return (str(int(delta.days//dpm)) +' months')
    elif delta.days > 7:
        if delta.days//7 == 1:
            return ('1 week')
        else:
            return (str(delta.days//7) +' weeks')
    elif delta.days > 0:
        if delta.days == 1:
            return ("1 day")
        else:
            return (str(delta.days) + ' days')
    elif delta.seconds > 3600:
        if delta.seconds//3600 == 1:
            return('1 hour')
        else:
            print(today, post_date, delta.seconds/3600)
            return (str(delta.seconds//3600) + ' hours')
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

def remove_expired_posts(conn):
    """
    Remove expired posts from the database.
    """
    curs = dbi.dict_cursor(conn)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        DELETE FROM post
        WHERE expiration_date < %s
    """
    curs.execute("DELETE FROM rating WHERE post_id IN (SELECT post_id FROM post WHERE expiration_date < %s)", (current_date,))
    curs.execute(query, [current_date])
    conn.commit()
    
def insert_comment(conn, post_id, user_email, comment):
    '''
    Inserts comment to a post into table
    '''
    curs = dbi.dict_cursor(conn)
    now = datetime.now()
    commentDate = now.strftime('%Y-%m-%d %H:%M:%S')
    
    curs.execute('''insert into comments(post_id, user_email, comment, date)
                    values(%s, %s, %s, %s)''',
                    [post_id, user_email, comment, commentDate])

    # query = "INSERT INTO comments (post_id, user_email, comment, date) VALUES ((%s, %s, %s, %s)"
    # values=[post_id, user_email, comment, commentDate]
    # curs.execute(query, values)
    conn.commit()

def get_comments_for_post(conn, post_id):
    '''
    gets the comments for a post
    '''
    curs = dbi.dict_cursor(conn)
    query = "SELECT * FROM comments WHERE post_id=%s ORDER BY date DESC"
    curs.execute(query, [post_id])
    return curs.fetchall()



if __name__ == '__main__':
    db_to_use = 'wffa_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    conn = dbi.connect()
    # testing find_post_age()
    time = datetime(2023, 10, 23)
    print(find_post_age(time))
    # testing find_guide_ratings()
    print(find_guide_ratings(conn))
    print(find_guide_ratings(conn, 'kb102'))
    #print(display_posts(conn))