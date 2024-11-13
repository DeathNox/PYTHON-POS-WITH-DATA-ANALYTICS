-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: pos_new
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `tbl_purchase_order`
--

DROP TABLE IF EXISTS `tbl_purchase_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_purchase_order` (
  `purchase_order_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `sub_total` decimal(10,2) NOT NULL,
  `order_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `order_status` varchar(30) DEFAULT NULL,
  `item_name` varchar(50) DEFAULT NULL,
  `product_category` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`purchase_order_id`,`quantity`,`unit_price`,`sub_total`),
  UNIQUE KEY `purchase_order_id` (`purchase_order_id`),
  KEY `idx_purchase_order_id` (`purchase_order_id`),
  KEY `idx_purchase_order_sakes` (`quantity`),
  KEY `idx_purchase_order_unitPrice` (`unit_price`),
  KEY `idx_purchase_order_subTotal` (`sub_total`),
  KEY `idx_purchase_order_productName` (`item_name`),
  KEY `idx_purchase_order_productCategory` (`product_category`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_purchase_order`
--

LOCK TABLES `tbl_purchase_order` WRITE;
/*!40000 ALTER TABLE `tbl_purchase_order` DISABLE KEYS */;
INSERT INTO `tbl_purchase_order` VALUES (56,8,3,20.00,60.00,'2024-10-30 23:13:04','Completed','Test3','Iced coffee'),(57,14,3,30.00,90.00,'2024-10-30 23:13:38','Completed','Donut','Pastry'),(58,15,3,60.00,180.00,'2024-10-30 23:13:42','Completed','Sans Rival','Pastry'),(59,13,3,50.00,150.00,'2024-10-30 23:22:07','Completed','Carbonara','Pasta'),(60,16,8,30.00,240.00,'2024-10-31 16:38:28','Completed','Spaghetti','Pasta'),(61,10,9,30.00,270.00,'2024-10-31 21:14:49','Completed','Dinakdakan na Aso','Pasta'),(62,14,7,30.00,210.00,'2024-10-31 21:39:03','Completed','Donut','Pastry'),(63,15,6,60.00,360.00,'2024-10-31 21:46:12','Pending','Sans Rival','Pastry'),(64,15,10,60.00,600.00,'2024-10-31 21:47:19','Completed','Sans Rival','Pastry'),(65,15,10,60.00,600.00,'2024-10-31 21:47:19','Completed','Sans Rival','Pastry'),(66,17,6,40.00,240.00,'2024-10-31 21:51:40','Completed','Caramel','Iced coffee'),(67,14,1,30.00,30.00,'2024-11-02 00:54:23','Completed','Donut','Pastry'),(68,16,10,30.00,300.00,'2024-11-02 01:01:30','Completed','Spaghetti','Pasta'),(69,12,4,20.00,80.00,'2024-11-03 00:01:58','Completed','Cake','Pastry'),(70,10,1,30.00,30.00,'2024-11-08 12:38:36','Completed','Dinakdakan na Aso','Pasta'),(71,8,1,20.00,20.00,'2024-11-10 02:15:39','In Progress','Test3','Iced coffee'),(72,10,18,30.00,540.00,'2024-11-10 02:15:39','Completed','Dinakdakan na Aso','Pasta'),(73,9,1,30.00,30.00,'2024-11-11 00:43:25','Pending','Test2','Iced coffee'),(74,9,3,30.00,90.00,'2024-11-11 00:45:03','Completed','Test2','Iced coffee'),(75,14,1,30.00,30.00,'2024-11-11 00:47:34','Completed','Donut','Pastry'),(76,8,1,20.00,20.00,'2024-11-11 01:36:23','Completed','Test3','Iced coffee'),(77,9,1,30.00,30.00,'2024-11-12 17:04:39','Pending','Test2','Iced coffee'),(78,13,1,50.00,50.00,'2024-11-12 17:09:53','Pending','Carbonara','Pasta'),(79,10,1,30.00,30.00,'2024-11-12 18:28:35','Pending','Dinakdakan na Aso','Pasta'),(80,8,1,20.00,20.00,'2024-11-12 18:46:19','Pending','Test3','Iced coffee'),(81,15,1,60.00,60.00,'2024-11-12 20:40:43','Pending','Sans Rival','Pastry'),(82,9,1,30.00,30.00,'2024-11-12 20:44:54','Pending','Test2','Iced coffee'),(83,15,1,60.00,60.00,'2024-11-12 20:47:57','Pending','Sans Rival','Pastry'),(84,11,1,20.00,20.00,'2024-11-12 21:04:49','Pending','Test7','Iced coffee'),(85,17,1,40.00,40.00,'2024-11-12 21:05:16','Pending','Caramel','Iced coffee'),(86,10,1,30.00,30.00,'2024-11-12 21:07:23','Pending','Dinakdakan na Aso','Pasta'),(87,11,1,20.00,20.00,'2024-11-12 21:07:46','Pending','Test7','Iced coffee'),(88,10,1,30.00,30.00,'2024-11-12 21:08:49','Pending','Dinakdakan na Aso','Pasta'),(89,11,1,20.00,20.00,'2024-11-12 21:10:04','Pending','Test7','Iced coffee'),(90,11,1,20.00,20.00,'2024-11-12 21:13:50','Pending','Test7','Iced coffee'),(91,15,1,60.00,60.00,'2024-11-12 21:14:02','Pending','Sans Rival','Pastry'),(92,10,1,30.00,30.00,'2024-11-12 21:19:11','Pending','Dinakdakan na Aso','Pasta'),(93,11,1,20.00,20.00,'2024-11-12 21:31:53','Pending','Test7','Iced coffee'),(94,10,1,30.00,30.00,'2024-11-12 21:37:44','Pending','Dinakdakan na Aso','Pasta'),(95,11,1,20.00,20.00,'2024-11-12 21:38:07','Pending','Test7','Iced coffee'),(96,15,1,60.00,60.00,'2024-11-12 21:38:19','Pending','Sans Rival','Pastry'),(97,15,1,60.00,60.00,'2024-11-12 21:40:00','Pending','Sans Rival','Pastry'),(98,8,1,20.00,20.00,'2024-11-12 21:40:17','Pending','Test3','Iced coffee'),(99,18,1,50.00,50.00,'2024-11-13 16:52:48','Pending','Spaghetti','Pasta'),(100,18,1,50.00,50.00,'2024-11-13 16:56:51','Pending','Spaghetti','Pasta'),(101,12,1,20.00,20.00,'2024-11-13 16:59:36','Pending','Cake','Pastry'),(102,12,1,20.00,20.00,'2024-11-13 17:04:12','Pending','Cake','Pastry'),(103,18,1,50.00,50.00,'2024-11-13 17:05:48','Pending','Spaghetti','Pasta'),(104,18,1,50.00,50.00,'2024-11-13 17:06:11','Pending','Spaghetti','Pasta'),(105,18,1,50.00,50.00,'2024-11-13 17:07:11','Pending','Spaghetti','Pasta'),(106,18,1,50.00,50.00,'2024-11-13 17:07:36','Pending','Spaghetti','Pasta'),(107,12,1,20.00,20.00,'2024-11-13 17:08:39','Completed','Cake','Pastry'),(108,18,1,50.00,50.00,'2024-11-13 17:13:08','Pending','Spaghetti','Pasta'),(109,12,1,20.00,20.00,'2024-11-13 17:15:07','Pending','Cake','Pastry'),(110,18,1,50.00,50.00,'2024-11-13 17:29:19','Pending','Spaghetti','Pasta'),(111,18,3,50.00,150.00,'2024-11-13 17:30:36','Completed','Spaghetti','Pasta'),(112,18,1,50.00,50.00,'2024-11-13 17:45:17','Pending','Spaghetti','Pasta'),(113,18,1,50.00,50.00,'2024-11-13 17:46:03','Pending','Spaghetti','Pasta'),(114,12,1,20.00,20.00,'2024-11-13 17:46:03','Pending','Cake','Pastry'),(115,18,1,50.00,50.00,'2024-11-13 17:58:43','Pending','Spaghetti','Pasta');
/*!40000 ALTER TABLE `tbl_purchase_order` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-13 18:24:46
