drop table if exists picture; 
drop table if exists rating;
drop table if exists post;
drop table if exists user;

CREATE TABLE `user` (
  `user_email` char(8) PRIMARY KEY COMMENT 'Unique identifier for each user',
  `name` varchar(50) COMMENT 'Name of the user',
  `join_date` timestamp COMMENT 'Joined date for the user',
  `food_guide` boolean COMMENT 'Whether user is a food guide or not',
  `post_count` integer COMMENT 'number of posts overall'
);

CREATE TABLE `post` (
  `post_id` integer PRIMARY KEY COMMENT 'Unique identifier for each food post',
  `user_email` char(8) COMMENT 'email of guide who made the post',
  `description` text COMMENT 'Detail field for the free food',
  `post_date` timestamp COMMENT 'when the post was created',
  `expiration_date` timestamp COMMENT 'when the post should be deleted',
  `location` varchar(6) COMMENT 'Specific room location of the food',
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
  `allergens` ENUM ('soy', 'peanuts', 'dairy', 'gluten', 'egg', 'shellfish', 'nuts', 'sesame') COMMENT 'list of allergens present in the food'
);

CREATE TABLE `rating` (
  `rate_id` integer PRIMARY KEY COMMENT 'unique id of this rating, could be replaced with triple of guide, rater, and post',
  `post_id` integer COMMENT 'ID of the post being rated',
  `guide_email` char(8) COMMENT 'email of the guide being rated',
  `rater_email` char(8) COMMENT 'email of the user making the rating',
  `rating` ENUM ('1', '2', '3', '4', '5') COMMENT 'star-value of the rating'
);

CREATE TABLE `picture` (
  `post_id` integer COMMENT 'post id that images are associated with',
  `image_id` integer AUTO_INCREMENT COMMENT 'unique image id',
  `picture` IMAGE COMMENT 'Image of food item',
  PRIMARY KEY (`post_id`, `image_id`)
);

ALTER TABLE `post` ADD FOREIGN KEY (`user_email`) REFERENCES `user` (`user_email`);

ALTER TABLE `rating` ADD FOREIGN KEY (`guide_email`) REFERENCES `user` (`user_email`);

ALTER TABLE `rating` ADD FOREIGN KEY (`rater_email`) REFERENCES `user` (`user_email`);

ALTER TABLE `rating` ADD FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`);

ALTER TABLE `image` ADD FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`);