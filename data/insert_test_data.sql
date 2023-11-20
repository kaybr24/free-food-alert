use wffa_db;

insert into user(`user_email`, `name`, `join_date`, `food_guide`, `post_count`)
values
	('kb102', 'Kayla Brand', '11-06-23', True, 0),
    ('fy100', 'Jennifer Yu', '01-08-02', False, 0),
    ('kw102', 'Kayley Wang', '29-05-24', True, 30),
    ('mm999', 'Mickey Mouse', '23-12-10', False, 0);

insert into post(`post_id`, `user_email`, `description`, `post_date`, `expiration_date`, `location`, `building`, `allergens`)
values
    (NULL, 'kw102', 'marshmallows, chocolate, and graham crackers', NOW(), '23-11-30', 'Bates Living Room', 'Bates Hall', 'gluten'),
    (NULL, 'mm999', 'cheese', '00-01-01', NULL, 'room 413', 'Lulu Chow Wang Campus Center', NULL), 
    (NULL, 'kb102', 'bagels and lox', '23-11-20', '24-01-01', 'ASTRO conference room', 'Observatory', 'eggs,gluten,sesame,dairy');


insert into rating(`rate_id`, `post_id`, `guide_email`, `rater_email`, `rating`)
values
    (NULL, 3, 'kb102', 'fy100', 4),
    (NULL, 3, 'kb102', 'mm999', 5);

insert into `picture`(`post_id`, `image_id`);
values
    (1, 0), /*ERROR: auto-increment is not working?*/
    (1, 1),
    (3, 2);

    