USE wffa_db;

DROP TABLE if exists `picture`;

CREATE TABLE `picture` (
  `user_email` varchar(30) not null COMMENT 'lasting responsibility identifier',
  `post_id` integer COMMENT 'post id that images are associated with',
  `image_id` integer not null AUTO_INCREMENT COMMENT 'unique id for image of food item',
  `filetype` varchar(10) not null COMMENT 'file ending',
  PRIMARY KEY (`image_id`),
  foreign key (post_id) references `post`(post_id) 
        on delete cascade on update cascade
);

ALTER TABLE `picture` ADD FOREIGN KEY (`user_email`) REFERENCES `user` (`user_email`) on delete cascade on update cascade;

ALTER TABLE `picture` ADD FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) on delete cascade on update cascade;