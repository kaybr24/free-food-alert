use wffa_db;

drop table if exists picture; 
drop table if exists rating;
drop table if exists post;
drop table if exists user;

CREATE TABLE `user` (
  `user_email` varchar(30) PRIMARY KEY COMMENT 'Unique identifier for each user',
  `name` varchar(50) COMMENT 'Name of the user',
  `join_date` timestamp COMMENT 'Joined date for the user',
  `password` char(60) COMMENT 'bcrypt encoded password',
  `food_guide` boolean COMMENT 'Whether user is a food guide or not',
  `post_count` integer COMMENT 'number of posts overall'
);

CREATE TABLE `post` (
  `post_id` integer PRIMARY KEY not null AUTO_INCREMENT COMMENT 'Unique identifier for each food post',
  `user_email` varchar(30) COMMENT 'email of guide who made the post',
  `description` text COMMENT 'Detail field for the free food',
  `post_date` timestamp COMMENT 'when the post was created',
  `expiration_date` timestamp COMMENT 'when the post should be deleted',
  `location` varchar(30) COMMENT 'Specific room location of the food',
  `building` ENUM ('Acorns', 'Alumnae Hall', 'Athletic Maintenance Facility', 'Bates Hall', 
    'Beebe Hall', 'Billings', 'Boathouse', 'Campus Police Headquarters', 'Cazenove Hall', 
    'Cedar Lodge', 'Cervantes', 'Cheever House', 'Child Study Center', 'Claflin Hall', 
    'Collins Cinema', 'Continuing Education Office', 'Davis Hall', 'Davis Museum', 
    'Davis Parking Facility', 'Day Care Center', 'Distribution Center', 'Dower House', 
    'East Lodge', 'Fiske House', 'Founders Hall', 'Freeman Hall', 'French House - Carriage', 
    'French House - Main', 'Golf House', 'Green Hall', 'Grounds', 'Hallowell House', 'Harambee House', 
    'Hemlock', 'Homestead', 'Horton House', 'Instead', 'Jewett Art Center', 'Keohane Sports Center', 
    'Lake House', 'Library', 'Lulu Chow Wang Campus Center', 'Margaret Ferguson Greenhouses', 
    'McAfee Hall', 'Motor Pool', 'Munger Hall', 'Nehoiden House', 'Observatory', 'Orchard Apts', 
    'Pendleton Hall East', 'Pendleton Hall West', 'Physical Plant', 'Pomeroy Hall', 
    "President's House", 'Ridgeway Apts', 'Schneider Center', 'Science Center', 'Service Building', 
    'Severance Hall', 'Shafer Hall', 'Shakespeare', 'Shepard House', 'Simpson Hall', 'Simpson West', 
    'Slater International Center', 'Stone Center', 'Stone Hall', 'Tower Court East', 'Tower Court West',
     'Trade Shops Building', 'Tau Zeta Epsilon', 'Waban House', 'Weaver House', 'Webber Cottage', 
     'Wellesley College Club', 'West Lodge', 'Whitin House', 'Zeta Alpha House') 
     COMMENT 'Select one Wellesley campus building where the food is located',
  `allergens` SET ('soy', 'peanuts', 'dairy', 'gluten', 'eggs', 'shellfish', 'nuts', 'sesame') COMMENT 'list of allergens present in the food'
);

CREATE TABLE `rating` (
  `post_id` integer COMMENT 'ID of the post being rated',
  `guide_email` varchar(30) COMMENT 'email of the guide being rated',
  `rater_email` varchar(30) COMMENT 'email of the user making the rating',
  `rating` ENUM ('1', '2', '3', '4', '5') COMMENT 'star-value of the rating',
  PRIMARY KEY (`post_id`, `guide_email`, `rater_email`)
);

CREATE TABLE `picture` (
  `user_email` varchar(30) COMMENT 'lasting responsibility identifier',
  `post_id` integer COMMENT 'post id that images are associated with',
  `image_id` integer not null AUTO_INCREMENT COMMENT 'unique id for image of food item',
  PRIMARY KEY (`user_email`, `image_id`),
  foreign key (post_id) references `post`(post_id) 
        on delete cascade on update cascade
);

ALTER TABLE `post` ADD FOREIGN KEY (`user_email`) REFERENCES `user` (`user_email`) on delete cascade on update cascade;

ALTER TABLE `rating` ADD FOREIGN KEY (`guide_email`) REFERENCES `user` (`user_email`) on delete cascade on update cascade;

ALTER TABLE `rating` ADD FOREIGN KEY (`rater_email`) REFERENCES `user` (`user_email`) on delete cascade on update cascade;

ALTER TABLE `rating` ADD FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) on update cascade;

ALTER TABLE `picture` ADD FOREIGN KEY (`user_email`) REFERENCES `user` (`user_email`) on delete cascade on update cascade;

ALTER TABLE `picture` ADD FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) on delete cascade on update cascade;
