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