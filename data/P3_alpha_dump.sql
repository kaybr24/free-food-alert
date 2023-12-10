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
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) DEFAULT NULL,
  `user_email` varchar(30) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`comment_id`),
  KEY `post_id` (`post_id`),
  KEY `user_email` (`user_email`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_email`) REFERENCES `user` (`user_email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (3,7,'ss102','woohoo!','2023-12-05 20:39:13'),(4,7,'dw102','is it good?','2023-12-05 20:39:40'),(6,7,'dw102','blah blah','2023-12-05 20:40:50'),(8,7,'dw102','testing scrollabiltiy...','2023-12-05 20:42:09'),(9,7,'dw102','will the comments scroll?\r\n','2023-12-05 20:42:18'),(10,7,'dw102','pllleaassee scroll!','2023-12-05 20:42:29'),(11,7,'dw102','food webstie','2023-12-05 20:42:41'),(14,7,'dw102','testing comment size and how it will appear on the box.............................................................','2023-12-05 20:48:57'),(15,7,'dw102','add comment\r\n','2023-12-05 20:57:00'),(16,7,'mc104','oh, hello!\r\n','2023-12-06 00:04:37'),(17,10,'dw102','oh no!','2023-12-06 15:07:46'),(18,7,'tl001','The ice cubes aren\'t very flavorable \\(`0\')/','2023-12-10 15:39:07'),(19,12,'tl001','Where is Billings -1?','2023-12-10 15:49:38');
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `picture`
--

LOCK TABLES `picture` WRITE;
/*!40000 ALTER TABLE `picture` DISABLE KEYS */;
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
  `user_email` varchar(30) DEFAULT NULL COMMENT 'email of guide who made the post',
  `description` text DEFAULT NULL COMMENT 'Detail field for the free food',
  `post_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'when the post was created',
  `expiration_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'when the post should be deleted',
  `location` varchar(30) DEFAULT NULL COMMENT 'Specific room location of the food',
  `building` enum('Acorns','Alumnae Hall','Athletic Maintenance Facility','Bates Hall','Beebe Hall','Billings','Boathouse','Campus Police Headquarters','Cazenove Hall','Cedar Lodge','Cervantes','Cheever House','Child Study Center','Claflin Hall','Collins Cinema','Continuing Education Office','Davis Hall','Davis Museum','Davis Parking Facility','Day Care Center','Distribution Center','Dower House','East Lodge','Fiske House','Founders Hall','Freeman Hall','French House - Carriage','French House - Main','Golf House','Green Hall','Grounds','Hallowell House','Harambee House','Hemlock','Homestead','Horton House','Instead','Jewett Art Center','Keohane Sports Center','Lake House','Library','Lulu Chow Wang Campus Center','Margaret Ferguson Greenhouses','McAfee Hall','Motor Pool','Munger Hall','Nehoiden House','Observatory','Orchard Apts','Pendleton Hall East','Pendleton Hall West','Physical Plant','Pomeroy Hall','President''s House','Ridgeway Apts','Schneider Center','Science Center','Service Building','Severance Hall','Shafer Hall','Shakespeare','Shepard House','Simpson Hall','Simpson West','Slater International Center','Stone Center','Stone Hall','Tower Court East','Tower Court West','Trade Shops Building','Tau Zeta Epsilon','Waban House','Weaver House','Webber Cottage','Wellesley College Club','West Lodge','Whitin House','Zeta Alpha House') DEFAULT NULL COMMENT 'Select one Wellesley campus building where the food is located',
  `allergens` set('soy','peanuts','dairy','gluten','eggs','shellfish','nuts','sesame') DEFAULT NULL COMMENT 'list of allergens present in the food',
  PRIMARY KEY (`post_id`),
  KEY `user_email` (`user_email`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_email`) REFERENCES `user` (`user_email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (3,'kb102','bagels and lox','2023-11-20 05:00:00','2024-01-01 05:00:00','ASTRO conference room','Observatory','dairy,gluten,eggs,sesame'),(7,'mc104','ice cubes','2023-12-04 05:00:00','2023-12-25 19:09:00','Tower Dining Hall','Tower Court East',''),(10,'dw102','testing food!','2023-12-06 05:00:00','2024-01-04 15:01:00','111','Child Study Center','peanuts'),(12,'tl001','warm cheesy lemon ricotta Italian pancakes with raspberry jam','2023-12-10 15:49:15','2023-12-16 03:48:00','-1','Billings','dairy,gluten,eggs');
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rating`
--

DROP TABLE IF EXISTS `rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rating` (
  `post_id` int(11) NOT NULL COMMENT 'ID of the post being rated',
  `guide_email` varchar(30) NOT NULL COMMENT 'email of the guide being rated',
  `rater_email` varchar(30) NOT NULL COMMENT 'email of the user making the rating',
  `rating` enum('1','2','3','4','5') DEFAULT NULL COMMENT 'star-value of the rating',
  PRIMARY KEY (`post_id`,`guide_email`,`rater_email`),
  KEY `guide_email` (`guide_email`),
  KEY `rater_email` (`rater_email`),
  CONSTRAINT `rating_ibfk_1` FOREIGN KEY (`guide_email`) REFERENCES `user` (`user_email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `rating_ibfk_2` FOREIGN KEY (`rater_email`) REFERENCES `user` (`user_email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `rating_ibfk_3` FOREIGN KEY (`post_id`) REFERENCES `post` (`post_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rating`
--

LOCK TABLES `rating` WRITE;
/*!40000 ALTER TABLE `rating` DISABLE KEYS */;
INSERT INTO `rating` VALUES (3,'kb102','dw102','5'),(3,'kb102','mc104','2'),(7,'mc104','tl001','1'),(10,'dw102','tl001','4');
/*!40000 ALTER TABLE `rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_email` varchar(30) NOT NULL COMMENT 'Unique identifier for each user',
  `name` varchar(50) DEFAULT NULL COMMENT 'Name of the user',
  `join_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Joined date for the user',
  `password` char(60) DEFAULT NULL COMMENT 'bcrypt encoded password',
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
INSERT INTO `user` VALUES ('ap555','Alphie Pine','2023-12-02 05:00:00','$2b$12$cgRo6qrWgz6LHIGsJHhDC.ulYrOMA4kLLVUUQwTNjT23son8pYiou',NULL,NULL),('dw102','Dayle Wang','2023-12-06 15:12:32','$2b$12$McahQUPr8ckkIs7xJFMnd.55VGlCkL7KEBAbRtOwjFHrY35o9RFrq',1,4),('fy100','Jennifer Yu','2001-08-02 04:00:00',NULL,0,0),('fy101','Jennifer Yu','2023-12-02 05:00:00','$2b$12$.rSEMhtTs22lhggIdyoBSuRmcDcRZmzVANR3lzr5IA1XTchVeJ2Um',NULL,NULL),('kb102','Kayla Brand','2011-06-23 04:00:00',NULL,1,0),('kw102','Kayley Wang','2029-05-24 04:00:00',NULL,1,30),('mc104','Marsha Cooper','2023-12-04 19:09:33','$2b$12$smTDEVBsbKffqUA7zTHNc.5.wPjafi4dBXV0hfMBI64J2V/KYgXvO',1,2),('mm999','Mickey Mouse','2023-12-10 05:00:00',NULL,0,0),('oi60','Omashu III','2023-12-02 05:00:00','$2b$12$2zrHnfoV2taXt7qIyjt6e.XqHWF7Uws05H2cErPsZtpNB8a72uzjG',NULL,NULL),('sm105','Sam Man','2023-12-02 05:00:00','$2b$12$guitMyyLT6G79LKyh6DfFe/9b3U3tR.Sll9PdoYvO3obWDwfz1iei',NULL,NULL),('ss102','Susan Sally','2023-12-04 20:00:44','$2b$12$upU8IofsWYDPaDO9SOW5COXauiEHCjQvbouwjGvo/nClbrBwFm0te',1,2),('sw113','Sarai Willkuma','2023-12-02 05:00:00','$2b$12$zHIs8D4HK0y1xM9xWCT/4uvbTVoPRrVgaww7qE.FsCCpx2jmc0JCq',NULL,NULL),('ta111','Tahani Al-Jamil','2023-12-02 05:00:00','$2b$12$RIw.Y8kl91z2YgJIbKYVQuu.XADueVNdn.8BWJdmF.1TncVEtJ1h.',NULL,NULL),('test111','test111','2023-12-05 05:00:00','$2b$12$YFGimGZcc1RFjjhComugHOEkS0QwloLPv85uMw4m9nAYBbpB2lRku',NULL,NULL),('tl001','Tupelo Lane','2023-12-10 15:49:15','$2b$12$OLKOMcBZ77Cyzff/5VYmfuMRG9cnGcAH7pO2ZpGN91mEkzUlLvHBa',1,1),('tt111','test 1','2023-12-02 05:00:00','$2b$12$lHtA6zyV1dJH21Y73v0NQOXyZqx/7Rpf4JeseEAm3pkSmvvfk23kq',NULL,NULL);
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

-- Dump completed on 2023-12-10 11:21:45
