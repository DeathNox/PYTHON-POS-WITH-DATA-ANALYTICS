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
-- Table structure for table `tbl_sales`
--

DROP TABLE IF EXISTS `tbl_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_sales` (
  `sales_id` int NOT NULL AUTO_INCREMENT,
  `invoice_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `product_name` varchar(50) DEFAULT NULL,
  `product_category` varchar(100) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `unit_price` decimal(10,2) DEFAULT NULL,
  `sub_total` decimal(10,2) DEFAULT NULL,
  `order_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sales_id`),
  KEY `fk_product_sales_id` (`product_id`),
  KEY `fk_product_sales_quantity` (`quantity`),
  KEY `fk_product_sales_unitPrice` (`unit_price`),
  KEY `fk_product_sales_subTotal` (`sub_total`),
  KEY `fk_product_sales_productName` (`product_name`),
  KEY `fk_product_sales_productCategory` (`product_category`),
  CONSTRAINT `fk_product_sales_id` FOREIGN KEY (`product_id`) REFERENCES `tbl_products` (`product_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_product_sales_productCategory` FOREIGN KEY (`product_category`) REFERENCES `tbl_purchase_order` (`product_category`) ON DELETE CASCADE,
  CONSTRAINT `fk_product_sales_productName` FOREIGN KEY (`product_name`) REFERENCES `tbl_purchase_order` (`item_name`) ON DELETE CASCADE,
  CONSTRAINT `fk_product_sales_quantity` FOREIGN KEY (`quantity`) REFERENCES `tbl_purchase_order` (`quantity`) ON DELETE CASCADE,
  CONSTRAINT `fk_product_sales_subTotal` FOREIGN KEY (`sub_total`) REFERENCES `tbl_purchase_order` (`sub_total`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_sales`
--

LOCK TABLES `tbl_sales` WRITE;
/*!40000 ALTER TABLE `tbl_sales` DISABLE KEYS */;
INSERT INTO `tbl_sales` VALUES (53,1,8,'Test3','Iced coffee',3,20.00,60.00,'2024-11-02 00:52:16'),(54,2,14,'Donut','Pastry',3,30.00,90.00,'2024-11-02 00:52:16'),(55,3,15,'Sans Rival','Pastry',3,60.00,180.00,'2024-11-02 00:52:16'),(56,4,13,'Carbonara','Pasta',3,50.00,150.00,'2024-11-02 00:52:16'),(57,5,16,'Spaghetti','Pasta',8,30.00,240.00,'2024-11-02 00:52:16'),(58,6,10,'Dinakdakan na Aso','Pasta',9,30.00,270.00,'2024-11-02 00:52:16'),(59,7,14,'Donut','Pastry',7,30.00,210.00,'2024-11-02 00:52:16'),(60,8,15,'Sans Rival','Pastry',10,60.00,600.00,'2024-11-02 00:52:16'),(61,9,15,'Sans Rival','Pastry',10,60.00,600.00,'2024-11-02 00:52:16'),(62,10,17,'Caramel','Iced coffee',6,40.00,240.00,'2024-11-02 00:52:16'),(63,11,14,'Donut','Pastry',1,30.00,30.00,'2024-11-02 00:54:28'),(64,12,16,'Spaghetti','Pasta',10,30.00,300.00,'2024-11-02 01:01:34'),(65,13,12,'Cake','Pastry',4,20.00,80.00,'2024-11-03 00:02:06'),(66,14,12,'Cake','Pastry',4,20.00,80.00,'2024-11-03 00:02:08');
/*!40000 ALTER TABLE `tbl_sales` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-03  0:12:21
