#Kayley's search file with queries 
import cs304dbi as dbi
from datetime import datetime


def search_for_post(conn, searched_item):
    """
    Given a dictionary if items searched for by the user, 
    finds if there are any posts with specified search
    and returns the post.
    """
    curs = dbi.dict_cursor(conn)

    query = "SELECT * FROM post WHERE"

    if len(searched_item['location'])>0:
        l = searched_item['location']
        locations=tuple(x for x in l)
        query += " building IN {}".format(locations).replace(',)', ')')
    

    if len(searched_item['allergens'])>0:
        allergens = tuple(searched_item['allergens'])
        if 'building' in query:
            query += " AND allergens not in {}".format(allergens).replace(',)', ')')
        else:
             query += " allergens not in {}".format(allergens).replace(',)', ')')

    if searched_item['date_posted']:
        formatted_date = datetime.strptime(searched_item['date_posted'], '%Y-%m-%d').strftime('%Y-%m-%d')

        if 'building' in query or 'allergens' in query:
            query += " AND post_date = '{}'".format(formatted_date)
        else:
            query += " post_date = '{}'".format(formatted_date)
      
    if query == "SELECT * FROM post WHERE":
        query = "SELECT * from post"
        
    curs.execute(query)

    data = curs.fetchall()
    return data

