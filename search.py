#Kayley's search file with queries 
import cs304dbi as dbi

def search_for_post(conn, searched_item):
    """
    Given a dictionary if items searched for by the user, 
    finds if there are any posts with specified search
    and returns the post.
    """
    curs = dbi.dict_cursor(conn)
    query = "SELECT * FROM food_table WHERE location=%s AND allergens=%s AND date_posted=%s"
    curs.execute(query, (location, allergens, date_posted))
    data = cursor.fetchall()

if __name__ == '__main__':
    db_to_use = 'wffa_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    conn = dbi.connect()
    searched_item = {'location': ['Lulu'],
                        'allergens': ['eggs'],
                        'date_posted': ""}
    print(search_for_post(conn, searched_item))
