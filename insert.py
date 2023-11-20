import cs304dbi as dbi

def insert_post(conn, user_email, description, post_date, expiration_date, location, building, allergens):
    curs = dbi.dict_cursor(conn)
   

    curs.execute('''insert into post(user_email, description, post_date, expiration_date, location, building, allergens)
                    values(%s, %s, %s, %s, %s, %s, %s)''',
                    [user_email, description, post_date, expiration_date, location, building, ','.join(allergens)])
    conn.commit()


# insert into post(`post_id`, `user_email`, `description`, `post_date`, `expiration_date`, `location`, `building`, `allergens`)
# values
#     (NULL, 'kw102', 'marshmallows, chocolate, and graham crackers', NOW(), '23-11-30', 'Bates Living Room', 'Bates Hall', 'gluten'),
#     (NULL, 'mm999', 'cheese', '00-01-01', NULL, 'room 413', 'Lulu Chow Wang Campus Center', NULL), 
#     (NULL, 'kb102', 'bagels and lox', '23-11-20', '24-01-01', 'ASTRO conference room', 'Observatory', 'eggs,gluten,sesame,dairy');

