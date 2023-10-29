CREATE TABLE `user` (
  `user_email` char(5) PRIMARY KEY,
  `name` varchar(50),
  `join_date` timestamp,
  `food_guide` boolean,
  `post_num` integar
);

CREATE TABLE `post` (
  `post_id` integer PRIMARY KEY,
  `user_email` char(5),
  `description` text,
  `post_date` timestamp,
  `expiration_date` timestamp,
  `location` text,
  `allergens` ENUM ('soy', 'peanuts', 'dairy', 'gluten', 'egg', 'shellfish', 'nuts', 'sesame'),
  `picture` IMAGE
);

CREATE TABLE `rating` (
  `rate_id` integar PRIMARY KEY,
  `post_id` integar,
  `user_email` char(5),
  `rater` char(5),
  `rate` integar,
  `post` integer
);

ALTER TABLE `post` ADD FOREIGN KEY (`user_email`) REFERENCES `user` (`user_email`);

ALTER TABLE `rating` ADD FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`);

ALTER TABLE `rating` ADD FOREIGN KEY (`user_email`) REFERENCES `user` (`user_email`);

ALTER TABLE `rating` ADD FOREIGN KEY (`rater`) REFERENCES `user` (`user_email`);
