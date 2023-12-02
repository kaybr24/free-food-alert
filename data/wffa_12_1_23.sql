-- MariaDB dump 10.19  Distrib 10.5.22-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: wffa_db
-- ------------------------------------------------------
-- Server version	10.5.22-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `picture`
--

DROP TABLE IF EXISTS `picture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `picture` (
  `post_id` int(11) DEFAULT NULL COMMENT 'post id that images are associated with',
  `image_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'unique id for image of food item',
  PRIMARY KEY (`image_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `picture_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `picture`
--

LOCK TABLES `picture` WRITE;
/*!40000 ALTER TABLE `picture` DISABLE KEYS */;
INSERT INTO `picture` VALUES (1,2);
/*!40000 ALTER TABLE `picture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for each food post',
  `user_email` char(8) DEFAULT NULL COMMENT 'email of guide who made the post',
  `description` text DEFAULT NULL COMMENT 'Detail field for the free food',
  `post_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'when the post was created',
  `expiration_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'when the post should be deleted',
  `location` varchar(30) DEFAULT NULL COMMENT 'Specific room location of the food',
  `building` enum('Acorns','Alumnae Hall','Athletic Maintenance Facility','Bates Hall','Beebe Hall','Billings','Boathouse','Campus Police Headquarters','Cazenove Hall','Cedar Lodge','Cervantes','Cheever House','Child Study Center','Claflin Hall','Collins Cinema','Continuing Education Office','Davis Hall','Davis Museum','Davis Parking Facility','Day Care Center','Distribution Center','Dower House','East Lodge','Fiske House','Founders Hall','Freeman Hall','French House - Carriage','French House - Main','Golf House','Green Hall','Grounds','Hallowell House','Harambee House','Hemlock','Homestead','Horton House','Instead','Jewett Art Center','Keohane Sports Center','Lake House','Library','Lulu Chow Wang Campus Center','Margaret Ferguson Greenhouses','McAfee Hall','Motor Pool','Munger Hall','Nehoiden House','Observatory','Orchard Apts','Pendleton Hall East','Pendleton Hall West','Physical Plant','Pomeroy Hall','President''s House','Ridgeway Apts','Schneider Center','Science Center','Service Building','Severance Hall','Shafer Hall','Shakespeare','Shepard House','Simpson Hall','Simpson West','Slater International Center','Stone Center','Stone Hall','Tower Court East','Tower Court West','Trade Shops Building','Tau Zeta Epsilon','Waban House','Weaver House','Webber Cottage','Wellesley College Club','West Lodge','Whitin House','Zeta Alpha House') DEFAULT NULL COMMENT 'Select one Wellesley campus building where the food is located',
  `allergens` set('soy','peanuts','dairy','gluten','eggs','shellfish','nuts','sesame') DEFAULT NULL COMMENT 'list of allergens present in the food',
  PRIMARY KEY (`post_id`),
  KEY `user_email` (`user_email`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_email`) REFERENCES `user` (`user_email`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,'kw102','marshmallows, chocolate, and graham crackers','2023-11-20 15:45:55','2023-11-30 05:00:00','Bates Living Room','Bates Hall','gluten'),(2,'mm999','cheese','2000-01-01 05:00:00','2023-11-20 15:45:55','room 413','Lulu Chow Wang Campus Center',NULL),(3,'kb102','bagels and lox','2023-11-20 05:00:00','2024-01-01 05:00:00','ASTRO conference room','Observatory','dairy,gluten,eggs,sesame'),(4,'kw102','ham and cheese','2023-11-20 05:00:00','2023-11-20 21:58:00','floor 1','Campus Police Headquarters',''),(5,'kw102','bananas, apples, pineapples, bread, walnut cake','2023-11-20 05:00:00','2023-11-21 22:03:00','333','Cervantes',''),(6,'kw102','Walnut banana bread - 1 loaf available (10 slices)','2023-11-20 05:00:00','2023-11-20 22:04:00','123','Acorns',''),(7,'kw102','grape jelly','2023-11-20 05:00:00','2023-11-20 22:38:00','in front of police station','Davis Parking Facility',''),(8,'rd100','delicious crumbs from puff pastries, baguettes, and sandwich bread, oh la la','2023-11-21 05:00:00','2023-11-30 23:14:00','front bench','Boathouse',''),(10,'sanderso','packaged twizzlers left over from Halloween','2023-11-25 05:00:00','2024-01-01 04:59:00','W118','Science Center',''),(11,'kw102','fruit cake with walnuts','2023-11-29 05:00:00','2023-11-30 18:29:00','333','Davis Hall',''),(12,'kw102','peanuts testing insert...','2023-11-29 05:00:00','2023-11-29 19:40:00','000','Claflin Hall',''),(13,'kw102','dairy?','2023-11-29 05:00:00','2023-11-30 22:41:00','33333','Continuing Education Office',''),(14,'kw102','peanuts!','2023-11-29 05:00:00','2023-12-01 22:42:00','321','Continuing Education Office',''),(15,'kw102','peanuts','2023-11-29 05:00:00','2023-11-29 21:49:00','111','Collins Cinema','peanuts,nuts'),(16,'kw102','Hot coffee and hot chocolate is available. Some milk on the side too.','2023-11-29 05:00:00','2023-12-01 00:00:00','122','Wellesley College Club','dairy'),(17,'ka111','Carrots, celery, broccoli','2023-11-29 05:00:00','2023-12-01 13:47:00','111','Davis Parking Facility',''),(18,'ka111','tofu stew with some nuts inside it?','2023-11-29 05:00:00','2023-11-30 02:53:00','1234','Collins Cinema','nuts'),(19,'ka111','tofu stew with some nuts inside it?','2023-11-29 05:00:00','2023-11-30 02:53:00','1234','Collins Cinema','nuts');
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rating`
--

DROP TABLE IF EXISTS `rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rating` (
  `rate_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'unique id of this rating, could be replaced with triple of guide, rater, and post',
  `post_id` int(11) DEFAULT NULL COMMENT 'ID of the post being rated',
  `guide_email` char(8) DEFAULT NULL COMMENT 'email of the guide being rated',
  `rater_email` char(8) DEFAULT NULL COMMENT 'email of the user making the rating',
  `rating` enum('1','2','3','4','5') DEFAULT NULL COMMENT 'star-value of the rating',
  PRIMARY KEY (`rate_id`),
  KEY `guide_email` (`guide_email`),
  KEY `rater_email` (`rater_email`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `rating_ibfk_1` FOREIGN KEY (`guide_email`) REFERENCES `user` (`user_email`),
  CONSTRAINT `rating_ibfk_2` FOREIGN KEY (`rater_email`) REFERENCES `user` (`user_email`),
  CONSTRAINT `rating_ibfk_3` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rating`
--

LOCK TABLES `rating` WRITE;
/*!40000 ALTER TABLE `rating` DISABLE KEYS */;
INSERT INTO `rating` VALUES (1,3,'kb102','fy100','4'),(2,3,'kb102','mm999','5'),(3,6,'kw102','rd100','3'),(4,2,'mm999','rd100','5'),(5,10,'sanderso','rd100','5'),(6,1,'kw102','rd100','5'),(7,14,'kw102','rd100','4'),(8,1,'kw102','rd100','5');
/*!40000 ALTER TABLE `rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_email` char(8) NOT NULL COMMENT 'Unique identifier for each user',
  `name` varchar(50) DEFAULT NULL COMMENT 'Name of the user',
  `password` char(60) DEFAULT NULL,
  `join_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Joined date for the user',
  `food_guide` tinyint(1) DEFAULT NULL COMMENT 'Whether user is a food guide or not',
  `post_count` int(11) DEFAULT NULL COMMENT 'number of posts overall',
  PRIMARY KEY (`user_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('fy100','Jennifer Yu',NULL,'2001-08-02 04:00:00',0,0),('ka111','Kelly Ann','$2b$12$SM8kIlFCc/wJUDrxPKQrOeVZ.03NCFc2yqghRQRcB8EE39sYzRh5K','2023-11-29 21:53:23',1,3),('kb102','Kayla Brand',NULL,'2011-06-23 04:00:00',1,0),('kw102','Kayley Wang',NULL,'2029-05-24 04:00:00',1,30),('mm999','Mickey Mouse',NULL,'2023-12-10 05:00:00',0,0),('rd100','Rubber Duck','$2b$12$k5ogteKD0UIZxX6xhL.Os.aPopUSVnpUoOBmVv7PRPFIuHn6zrMte','2023-12-01 22:50:55',1,NULL),('sanderso','Scott Anderson','$2b$12$XiCoWemtngIXqYabdvwCtefNk2TSY3.uY40xwZRZ8afhS10GuctMa','2023-11-25 05:00:00',NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-01 21:35:06
