CREATE DATABASE  IF NOT EXISTS `hr_dashboard` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `hr_dashboard`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: hr_dashboard
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `attendance_id` int NOT NULL AUTO_INCREMENT,
  `emp_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `login_time` datetime NOT NULL,
  `domain` varchar(55) NOT NULL,
  `timing` varchar(45) NOT NULL,
  PRIMARY KEY (`attendance_id`),
  KEY `emp_id` (`emp_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (51,1,'John Doe','2024-11-25 08:10:45','IT','On-Time'),(52,2,'Jane Smith','2024-11-25 08:15:30','HR','On-Time'),(53,3,'Alice Johnson','2024-11-25 08:20:15','Finance','On-Time'),(54,4,'Mark Brown','2024-11-25 08:25:00','Marketing','On-Time'),(55,5,'Emma Jones','2024-11-25 08:30:45','IT','On-Time'),(56,6,'Liam Wilson','2024-11-25 08:35:30','Operations','On-Time'),(57,7,'Sophia Davis','2024-11-25 08:40:15','IT','On-Time'),(58,8,'Oliver Garcia','2024-11-25 08:45:00','HR','Late'),(59,9,'Amelia White','2024-11-25 08:50:45','Finance','Late'),(60,10,'James Moore','2024-11-25 08:55:30','IT','Late'),(61,11,'Mia Taylor','2024-11-25 09:00:15','Marketing','Late'),(62,6,'Liam Wilson','2024-11-26 08:35:30','Operations','On-Time'),(63,8,'Oliver Garcia','2024-11-26 08:50:45','HR','Late'),(64,5,'Emma Jones','2024-11-26 08:30:45','IT','On-Time');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_percentage`
--

DROP TABLE IF EXISTS `attendance_percentage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_percentage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `month` varchar(45) NOT NULL,
  `attendance_percentage` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_percentage`
--

LOCK TABLES `attendance_percentage` WRITE;
/*!40000 ALTER TABLE `attendance_percentage` DISABLE KEYS */;
INSERT INTO `attendance_percentage` VALUES (1,'January',65),(2,'February',91),(3,'March',88),(4,'April',78),(5,'May',98),(6,'June',78),(7,'July',89),(8,'August',77),(9,'September',86),(10,'October',95),(11,'November',74),(12,'December',86);
/*!40000 ALTER TABLE `attendance_percentage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domains`
--

DROP TABLE IF EXISTS `domains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `domains` (
  `domain_id` int NOT NULL AUTO_INCREMENT,
  `domain_name` varchar(50) NOT NULL,
  PRIMARY KEY (`domain_id`),
  UNIQUE KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domains`
--

LOCK TABLES `domains` WRITE;
/*!40000 ALTER TABLE `domains` DISABLE KEYS */;
INSERT INTO `domains` VALUES (3,'Finance'),(2,'HR'),(1,'IT'),(4,'Marketing'),(5,'Operations');
/*!40000 ALTER TABLE `domains` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emp_locations`
--

DROP TABLE IF EXISTS `emp_locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emp_locations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `location` varchar(45) NOT NULL,
  `male_count` varchar(45) NOT NULL,
  `female_count` varchar(45) NOT NULL,
  `other_count` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emp_locations`
--

LOCK TABLES `emp_locations` WRITE;
/*!40000 ALTER TABLE `emp_locations` DISABLE KEYS */;
INSERT INTO `emp_locations` VALUES (1,'East Chennai','11','12','8'),(2,'West Chennai','26','12','4'),(3,'North Chennai','24','14','2'),(4,'West Chennai','29','15','7'),(5,'South Chennai','12','10','3'),(6,'North Chennai','18','11','5'),(7,'South Chennai','11','25','8'),(8,'North Chennai','21','10','5'),(9,'East Chennai','17','14','10'),(10,'North Chennai','22','16','2'),(11,'East Chennai','25','15','5'),(12,'West Chennai','30','20','9'),(13,'South Chennai','22','13','1'),(14,'North Chennai','15','9','2'),(15,'North Chennai','28','14','6');
/*!40000 ALTER TABLE `emp_locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `employee_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `age` int DEFAULT NULL,
  `mobile` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `emergency_contact` varchar(15) NOT NULL,
  `current_address` text NOT NULL,
  `permanent_address` text NOT NULL,
  `designation` varchar(50) NOT NULL,
  `shift` varchar(25) NOT NULL,
  `department` varchar(50) NOT NULL,
  `status` enum('Intern','Permanent','Temporary') DEFAULT NULL,
  `account_number` varchar(20) NOT NULL,
  `bank_name` varchar(50) NOT NULL,
  `ifsc_code` varchar(15) NOT NULL,
  `pan_number` varchar(15) NOT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Alice Johnson','1990-03-15','Female',34,'9876543210','alice.johnson@example.com','9876543211','123 St, City A','456 St, City A','Software Engineer','Morning','IT','Temporary','1234567890','HDFC Bank','HDFC0001234','ABCDE1234F'),(2,'Bob Smith','1985-07-20','Male',39,'9876543212','bob.smith@example.com','9876543213','789 St, City B','101 St, City B','Team Lead','Morning','HR','Permanent','9876543210','ICICI Bank','ICICI0005678','PQRST5678L'),(3,'Carla Williams','1992-05-22','Female',32,'9876543214','carla.williams@example.com','9876543215','234 St, City C','567 St, City C','HR Manager','Morning','HR','Intern','4567891230','Axis Bank','AXIS0003456','LMNOP9876Q'),(4,'David Brown','1988-11-05','Male',36,'9876543216','david.brown@example.com','9876543217','345 St, City D','678 St, City D','Marketing Executive','Night','Marketing','Intern','7891234560','SBI','SBIN0005678','GHJKL5678M'),(5,'Emily Davis','1995-02-10','Female',29,'9876543218','emily.davis@example.com','9876543219','456 St, City E','789 St, City E','Finance Analyst','Night','Finance','Permanent','1239876540','PNB','PNB0007890','UVWXY2345Z'),(6,'Franklin Miller','1989-08-13','Male',35,'9876543220','franklin.miller@example.com','9876543221','567 St, City F','890 St, City F','Operations Manager','Morning','Operations','Intern','9871234560','HDFC Bank','HDFC0005678','QRSTU5678L'),(7,'Grace Lee','1994-09-05','Female',30,'9876543222','grace.lee@example.com','9876543223','678 St, City G','901 St, City G','Marketing Specialist','Morning','Marketing','Permanent','6543219870','Axis Bank','AXIS0009876','WXYZT4567M'),(8,'Hannah Scott','1991-12-11','Female',31,'9876543224','hannah.scott@example.com','9876543225','789 St, City H','102 St, City H','HR Assistant','Morning','HR','Intern','3216549870','ICICI Bank','ICICI0004321','NOPQR3456Z'),(9,'Ian Clark','1987-03-30','Male',28,'9876543226','ian.clark@example.com','9876543227','890 St, City I','213 St, City I','Finance Manager','Morning','Finance','Intern','1236547890','PNB','PNB0001234','STUVW6789F'),(10,'Jessica Wright','1996-06-25','Female',28,'9876543228','jessica.wright@example.com','9876543229','901 St, City J','324 St, City J','IT Analyst','Night','IT','Permanent','9876543211','SBI','SBIN0003456','XYZAB1234C'),(11,'Evelyn Parker','1986-01-19','Female',38,'9876543260','evelyn.parker@example.com','9876543261','456 St, City X','678 St, City Y','Senior Developer','Night','IT','Temporary','2345678901','ICICI Bank','ICICI123456','GHJKA1234Q');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedbacks`
--

DROP TABLE IF EXISTS `feedbacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedbacks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `meeting_id` int NOT NULL,
  `employee_name` varchar(255) NOT NULL,
  `feedback` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `meeting_id` (`meeting_id`),
  CONSTRAINT `feedbacks_ibfk_1` FOREIGN KEY (`meeting_id`) REFERENCES `meetings` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedbacks`
--

LOCK TABLES `feedbacks` WRITE;
/*!40000 ALTER TABLE `feedbacks` DISABLE KEYS */;
INSERT INTO `feedbacks` VALUES (1,1,'John Doe','The HR meeting was insightful and helpful in understanding the company policies.'),(2,1,'Jane Smith','Good presentation, but I wish we had more time for questions.'),(3,2,'Alice Brown','The workshop was interactive, and I learned a lot of useful tools.'),(4,2,'Bob White','Great content, but it was a bit too long. A shorter duration would be better.'),(5,3,'Charlie Green','The team lunch was great for team bonding. The food could have been better though.'),(6,4,'David Black','The presentation on the new product features was clear and engaging.'),(7,5,'Eve Adams','The conference was informative, and the guest speakers were excellent.'),(8,6,'Frank Hill','I enjoyed the seminar, but the topic was a bit too broad. More focus would be appreciated.'),(9,7,'Grace Young','The webinar was very informative, especially the Q&A session.'),(10,8,'Hank Davis','Tools training was helpful for improving our technical skills. More hands-on examples would help.'),(11,9,'Ivy Lewis','The project status meeting was great for understanding the project’s current status and next steps.'),(12,10,'Jack Scott','The party was a wonderful way to celebrate achievements. The venue was excellent.');
/*!40000 ALTER TABLE `feedbacks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hiring`
--

DROP TABLE IF EXISTS `hiring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hiring` (
  `id` int NOT NULL AUTO_INCREMENT,
  `month` varchar(45) NOT NULL,
  `num_hirings` int NOT NULL,
  `num_terminations` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hiring`
--

LOCK TABLES `hiring` WRITE;
/*!40000 ALTER TABLE `hiring` DISABLE KEYS */;
INSERT INTO `hiring` VALUES (1,'Jan',200,120),(2,'Feb',190,110),(3,'Mar',180,100),(4,'Apr',160,90),(5,'May',150,80),(6,'June',140,70),(7,'July',130,60),(8,'Aug',120,50),(9,'Sep',100,40),(10,'Oct',90,30),(11,'Nov',80,20),(12,'Dec',70,10);
/*!40000 ALTER TABLE `hiring` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leave_requests`
--

DROP TABLE IF EXISTS `leave_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leave_requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `designation` varchar(50) NOT NULL,
  `leave_type` varchar(50) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `reason` text NOT NULL,
  `emp_name` varchar(255) NOT NULL,
  `status` enum('Pending','Accepted','Declined') NOT NULL DEFAULT 'Pending',
  PRIMARY KEY (`request_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `leave_requests_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leave_requests`
--

LOCK TABLES `leave_requests` WRITE;
/*!40000 ALTER TABLE `leave_requests` DISABLE KEYS */;
INSERT INTO `leave_requests` VALUES (1,2,'Team Lead','Annual Leave','2024-11-20','2024-11-24','Family vacation','Bob Smith','Pending'),(2,4,'HR Manager','Medical Leave','2024-11-18','2024-11-19','Medical treatment','David Brown','Pending'),(3,6,'Marketing Executive','Casual Leave','2024-11-25','2024-11-26','Personal work','Franklin Miller','Pending'),(4,8,'Finance Analyst','Annual Leave','2024-11-15','2024-11-20','Relocation process','Hannah Scott','Pending'),(5,10,'Operations Manager','Maternity Leave','2024-11-01','2024-11-30','Maternity leave','Jessica Wright','Pending');
/*!40000 ALTER TABLE `leave_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings`
--

DROP TABLE IF EXISTS `meetings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `date` date NOT NULL,
  `meet_url` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings`
--

LOCK TABLES `meetings` WRITE;
/*!40000 ALTER TABLE `meetings` DISABLE KEYS */;
INSERT INTO `meetings` VALUES (1,'HR Meeting','Room A','10:00:00','11:00:00','2024-11-01','https://meet.example.com/hr-meeting'),(2,'Workshop','Hall B','09:00:00','12:00:00','2024-11-03','https://meet.example.com/workshop'),(3,'Team Lunch','Cafeteria','12:30:00','14:00:00','2024-11-05','https://meet.example.com/team-lunch'),(4,'Presentation','Room D','15:00:00','16:30:00','2024-11-07','https://meet.example.com/presentation'),(5,'Conference','Room E','11:00:00','13:00:00','2024-11-10','https://meet.example.com/conference'),(6,'Seminar','Hall C','14:00:00','17:00:00','2024-11-15','https://meet.example.com/seminar'),(7,'Webinar','Online','09:00:00','10:30:00','2024-11-18','https://meet.example.com/webinar'),(8,'Tools Training','Hall A','10:00:00','11:00:00','2024-11-21','https://meet.example.com/tools-training'),(9,'Project Status Meeting','Room B','10:30:00','11:30:00','2024-11-27','https://meet.example.com/project-status'),(10,'Party For The Year Achievements','Hall A','14:00:00','16:00:00','2024-11-30','https://meet.example.com/party-achievements'),(17,'Project Kickoff Meeting','Conference Room A','09:00:00','10:00:00','2024-11-28','https://meet.example.com/kickoff'),(18,'Weekly Team Sync','Conference Room B','11:00:00','11:30:00','2024-11-29','https://meet.example.com/teamsync'),(20,'Development Standup','Google Meet','10:30:00','11:00:00','2024-12-01','https://meet.example.com/standup'),(22,'HR Orientation','Conference Room C','09:30:00','10:30:00','2024-12-03','https://meet.example.com/hr-orientation'),(23,'Operations Review','Microsoft Teams','15:00:00','16:00:00','2024-12-04','https://meet.example.com/operations-review'),(26,'Engineering Retrospective','Conference Room E','15:30:00','16:30:00','2024-11-26','https://meet.example.com/engineering-retrospective');
/*!40000 ALTER TABLE `meetings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission_requests`
--

DROP TABLE IF EXISTS `permission_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission_requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `emp_name` varchar(255) NOT NULL,
  `department` varchar(50) NOT NULL,
  `type_of_absence` varchar(50) NOT NULL,
  `reason` text NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `total_duration` time NOT NULL,
  `status` enum('Pending','Accepted','Declined') DEFAULT 'Pending',
  PRIMARY KEY (`request_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `permission_requests_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission_requests`
--

LOCK TABLES `permission_requests` WRITE;
/*!40000 ALTER TABLE `permission_requests` DISABLE KEYS */;
INSERT INTO `permission_requests` VALUES (1,1,'Alice Johnson','IT','Personal','Doctor appointment','2024-11-25 10:00:00','2024-11-25 12:00:00','02:00:00','Pending'),(2,3,'Carla Williams','HR','Personal','Family commitment','2024-11-24 14:00:00','2024-11-24 16:00:00','02:00:00','Pending'),(3,5,'Emily Davis','Finance','Official','Bank meeting','2024-11-23 09:00:00','2024-11-23 11:00:00','02:00:00','Pending'),(4,7,'Grace Lee','Marketing','Personal','Child’s school event','2024-11-22 13:00:00','2024-11-22 15:00:00','02:00:00','Pending'),(5,9,'Ian Clark','Operations','Official','Site visit','2024-11-21 10:00:00','2024-11-21 12:00:00','02:00:00','Pending');
/*!40000 ALTER TABLE `permission_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rolewise`
--

DROP TABLE IF EXISTS `rolewise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rolewise` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `role` varchar(45) NOT NULL,
  ` experience` varchar(45) NOT NULL,
  `skills` varchar(45) NOT NULL,
  `gender` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rolewise`
--

LOCK TABLES `rolewise` WRITE;
/*!40000 ALTER TABLE `rolewise` DISABLE KEYS */;
INSERT INTO `rolewise` VALUES (1,'Daniel Smith','Developer','3 years','Java,Spring Boot','Male'),(2,'Eva Johnson','Developer','1 year','HTML, CSS','Female'),(3,'Liam Williams','Designer','3 years','Figma, Sketch','Male'),(4,'Zoe Brown','Designer','5 years','Adobe XD, Photoshop','Female'),(5,'David Martinez','Data Scientist','2 years','R, Data Analysis','Male'),(6,'Sarah Garcia','Data Scientist','6 years','Machine Learning, Python','Female'),(7,'Chris Wilson','Data Scientist','4 years','Deep Learning, TensorFlow','Male'),(8,'Mason Anderson','Manager','5 years','Agile, Scrum','Male'),(9,'Lucas Thomas','Manager','7 years','Risk Management, Communication','Male'),(10,'Sophia Jackson','Manager','3 years','Team Leadership, Budgeting','Female'),(11,'Emma Davis','Business Analyst','4 years','Requirement Gathering, UML','Female'),(12,'Oliver Brown','Business Analyst','2 years','Data Analysis, SQL','Male'),(13,'Sophia Adams','Business Analyst','3 years','Stakeholder Management, Agile','Female'),(14,'Ethan Clark','Business Analyst','5 years','Business Process Mapping, Tableau','Male'),(15,'Zara','Tester','6 years','Python,AI','Female'),(16,'Peter','Tester','8 years','R,Java','Male'),(17,'Liya','Tester','4 years','SQL','Female'),(18,'John','Tester','7 years','Ruby,SQL','Male'),(19,'Tina','Tester','5years','Datascience','Female');
/*!40000 ALTER TABLE `rolewise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salary_distribution`
--

DROP TABLE IF EXISTS `salary_distribution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salary_distribution` (
  `id` int NOT NULL AUTO_INCREMENT,
  `department` varchar(50) DEFAULT NULL,
  `entry_level` int DEFAULT NULL,
  `junior` int DEFAULT NULL,
  `mid_level` int DEFAULT NULL,
  `senior` int DEFAULT NULL,
  `leader` int DEFAULT NULL,
  `manager` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salary_distribution`
--

LOCK TABLES `salary_distribution` WRITE;
/*!40000 ALTER TABLE `salary_distribution` DISABLE KEYS */;
INSERT INTO `salary_distribution` VALUES (1,'Engineering',60000,80000,100000,120000,140000,160000),(2,'Marketing',55000,75000,95000,115000,135000,155000),(3,'Sales',58000,78000,98000,118000,138000,158000);
/*!40000 ALTER TABLE `salary_distribution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `working_format`
--

DROP TABLE IF EXISTS `working_format`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `working_format` (
  `id` int NOT NULL AUTO_INCREMENT,
  `format` varchar(45) NOT NULL,
  `percentage` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `working_format`
--

LOCK TABLES `working_format` WRITE;
/*!40000 ALTER TABLE `working_format` DISABLE KEYS */;
INSERT INTO `working_format` VALUES (1,'onsite','30'),(2,'remote','40'),(3,'hybrid','25');
/*!40000 ALTER TABLE `working_format` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'hr_dashboard'
--

--
-- Dumping routines for database 'hr_dashboard'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-05 10:58:14
