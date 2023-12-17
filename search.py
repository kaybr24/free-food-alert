#Kayley's search file with queries 
import cs304dbi as dbi
from datetime import datetime
import information

legalAllergens = set(['soy', 'peanuts', 'dairy', 'gluten', 'eggs', 'shellfish', 'nuts', 'sesame'])
legalBuildings = set(information.locations)
# legalBuildings = set(['Acorns', 'Alumnae Hall', 'Athletic Maintenance Facility', 'Bates Hall', 
#     'Beebe Hall', 'Billings', 'Boathouse', 'Campus Police Headquarters', 'Cazenove Hall', 
#     'Cedar Lodge', 'Cervantes', 'Cheever House', 'Child Study Center', 'Claflin Hall', 
#     'Collins Cinema', 'Continuing Education Office', 'Davis Hall', 'Davis Museum', 
#     'Davis Parking Facility', 'Day Care Center', 'Distribution Center', 'Dower House', 
#     'East Lodge', 'Fiske House', 'Founders Hall', 'Freeman Hall', 'French House - Carriage', 
#     'French House - Main', 'Golf House', 'Green Hall', 'Grounds', 'Hallowell House', 'Harambee House', 
#     'Hemlock', 'Homestead', 'Horton House', 'Instead', 'Jewett Art Center', 'Keohane Sports Center', 
#     'Lake House', 'Library', 'Lulu Chow Wang Campus Center', 'Margaret Ferguson Greenhouses', 
#     'McAfee Hall', 'Motor Pool', 'Munger Hall', 'Nehoiden House', 'Observatory', 'Orchard Apts', 
#     'Pendleton Hall East', 'Pendleton Hall West', 'Physical Plant', 'Pomeroy Hall', 
#     "President's House", 'Ridgeway Apts', 'Schneider Center', 'Science Center', 'Service Building', 
#     'Severance Hall', 'Shafer Hall', 'Shakespeare', 'Shepard House', 'Simpson Hall', 'Simpson West', 
#     'Slater International Center', 'Stone Center', 'Stone Hall', 'Tower Court East', 'Tower Court West',
#      'Trade Shops Building', 'Tau Zeta Epsilon', 'Waban House', 'Weaver House', 'Webber Cottage', 
#      'Wellesley College Club', 'West Lodge', 'Whitin House', 'Zeta Alpha House'])

def search_for_post(conn, searched_item):
    """
    Given a dictionary if items searched for by the user, 
    finds if there are any posts with specified search
    and returns the post.
    """
    curs = dbi.dict_cursor(conn)

    query = """SELECT post_id, user_email, description, post_date, 
            expiration_date, location, building, allergens 
            FROM post WHERE"""

    if len(searched_item['building'])>0:
        l = searched_item['building']
        locations=tuple(x for x in l)
        for place in locations:
            if place not in legalBuildings: # data check against list of locations
                print(place)
                raise ValueError("illegal building")
                return None
        query += " building IN {}".format(locations).replace(',)', ')')
    

    if len(searched_item['allergens'])>0:
        allergens = [x.lower() for x in searched_item['allergens']]
        print("**************************************************")
        print(allergens)
        if 'building IN' in query:
            query += " AND"
        # check that allergens are legal
        if not set(allergens).issubset(legalAllergens):
            print(set(allergens), legalAllergens)
            raise ValueError('illegal allergen')
            return None
        # add to query
        for allergen in allergens:
            if allergen != allergens[0]:
                query += " AND"
            query += " (allergens not like '%{}%')".format(allergen) # this allergen is not listed

    if searched_item['date_posted']:
        formatted_date = datetime.strptime(searched_item['date_posted'], '%Y-%m-%d').strftime('%Y-%m-%d')

        if 'building' in query or 'allergens' in query:
            query += " AND post_date = '{}'".format(formatted_date)
        else:
            query += " post_date = '{}'".format(formatted_date)
      
    if query[-5:] == "WHERE":
        query = query[:-5] # remove "where" from query ending

    query += " ORDER BY post_date desc" # put newer postings on top
        
    print(query)
    curs.execute(query)

    data = curs.fetchall()
    return data

if __name__ == '__main__':
    db_to_use = 'wffa_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    conn = dbi.connect()
    if ("Bates Hall", "Tupelo Pool") not in legalBuildings: # data check against list of locations
        print("success")
    print ('gluten', not set(('gluten',)).issubset(legalAllergens))
    print ('gluten, rice', not set(('gluten', 'rice',)).issubset(legalAllergens))
    print ('rice', not set(('rice',)).issubset(legalAllergens))
    # print(
    #     ("Bates Hall") not in legalBuildings,
    #     ("Bates Hall", "Tupelo Pool") not in legalBuildings,
    #     ("Bates Hall", "Lulu Chow Wang Campus Center") not in legalBuildings,
    #     ("Bates Hall",) not in legalBuildings
    # )