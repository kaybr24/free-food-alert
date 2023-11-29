#Kayley's search file with queries 
import cs304dbi as dbi

def search_for_post(conn, searched_item):
    """
    Given a dictionary if items searched for by the user, 
    finds if there are any posts with specified search
    and returns the post.
    """
    curs = dbi.dict_cursor(conn)
    query = "SELECT * FROM post WHERE 1=1"

    if searched_item['location']:
        query += " AND location IN %(locations)s"

    if searched_item['allergens']:
        query += " AND allergens NOT IN %(allergens)s"

    if searched_item['date_posted']:
        query += " AND date_posted = %(date_posted)s"

    curs.execute(query, {'locations': searched_item['location'], 'allergens': searched_item['allergens'], 'date_posted': searched_item['date_posted']})
    data = curs.fetchall()
    return data

    
# if __name__ == '__main__':
#     db_to_use = 'wffa_db' 
#     print('will connect to {}'.format(db_to_use))
#     dbi.conf(db_to_use)
#     conn = dbi.connect()
#     searched_item = {'location': ['Lulu'],
#                         'allergens': ['eggs'],
#                         'date_posted': ""}
#     print(search_for_post(conn, searched_item))



