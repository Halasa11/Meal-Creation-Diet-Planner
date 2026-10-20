-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (arm64)
--
-- Host: localhost    Database: 
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Diet_Plan_Food`
--

DROP TABLE IF EXISTS `Diet_Plan_Food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Diet_Plan_Food` (
  `diet_plan_food_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `day` text,
  `meal_type` text,
  `food_id` int DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  PRIMARY KEY (`diet_plan_food_id`),
  KEY `user_id` (`user_id`),
  KEY `food_id` (`food_id`),
  CONSTRAINT `diet_plan_food_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `diet_plan_food_ibfk_2` FOREIGN KEY (`food_id`) REFERENCES `Food` (`food_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Diet_Plan_Food`
--

LOCK TABLES `Diet_Plan_Food` WRITE;
/*!40000 ALTER TABLE `Diet_Plan_Food` DISABLE KEYS */;
/*!40000 ALTER TABLE `Diet_Plan_Food` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Food`
--

DROP TABLE IF EXISTS `Food`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Food` (
  `food_id` int NOT NULL AUTO_INCREMENT,
  `food_item` text,
  `calories` int DEFAULT NULL,
  `carbohydrates` double DEFAULT NULL,
  `protein` double DEFAULT NULL,
  `fat` double DEFAULT NULL,
  `category` text,
  `diet` text,
  PRIMARY KEY (`food_id`)
) ENGINE=InnoDB AUTO_INCREMENT=408 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Food`
--

LOCK TABLES `Food` WRITE;
/*!40000 ALTER TABLE `Food` DISABLE KEYS */;
INSERT INTO `Food` VALUES (1,'Almonds',205,1.9,7.8,18.5,'breakfast','vegan'),(2,'Apples',43,10,0.5,0.4,'breakfast','vegan'),(3,'Apricots',31,7.2,0.9,0.1,'breakfast','vegan'),(4,'Asparagus',25,2,3.5,0.4,'lunch','vegan'),(5,'Aubergine',14,1.8,0.7,0.5,'lunch','vegan'),(6,'Avocado',189,1.9,2.1,19.3,'breakfast','vegan'),(7,'Baby Sweetcorn',31,4.6,2.2,0.6,'lunch','vegan'),(8,'Bacon Loin Steaks',158,1.1,28.9,4.3,'dinner',''),(9,'Bacon Rashers',295,0,24.2,22,'breakfast',''),(10,'Bagels',273,57.8,10,1.8,'breakfast','vegan'),(11,'Baked Beans canned in tomato sauce',81,15,5,0.5,'breakfast','vegan'),(12,'Baked Cassava',155,40.1,0.7,0.2,'lunch','vegan'),(13,'Baked Potato',97,22.6,2.5,0.2,'lunch','vegan'),(14,'Baked Salmon',232,0,25.2,14.6,'dinner','pescatarian'),(15,'Baked Sweet potato',115,27.9,1.6,0.4,'lunch','vegan'),(16,'Baked Tofu Burger',115,13.2,7.3,4,'lunch','vegan'),(17,'Baked Tuna',136,0,32.3,0.8,'lunch','pescatarian'),(18,'Bananas',81,20.3,1.2,0.1,'breakfast','vegan'),(19,'Beef Brisket',268,0,27.8,17.4,'lunch',''),(20,'Beef Sausages ',265,11,17.2,17.2,'lunch',''),(21,'Beetroot',53,11.6,1.6,0.3,'lunch','vegan'),(22,'Blackberries',27,5.6,1.1,0.2,'breakfast','vegan'),(23,'Bloater',251,0,23.5,17.4,'lunch','pescatarian'),(24,'Blueberries',40,9.1,0.9,0.2,'breakfast','vegan'),(25,'Boal',86,0,15.4,2.7,'lunch','pescatarian'),(26,'Boild Pasta ',159,31.8,6.6,1.5,'lunch','vegetarian'),(27,'Boiled Potato',74,17.5,1.8,0.1,'dinner','vegan'),(28,'Bombay Duck',283,0,61.7,4,'lunch',''),(29,'Braising Steak',246,0,32.9,12.7,'dinner',''),(30,'Brazil nuts',314,1.4,6.5,31.4,'lunch','vegan'),(31,'Breadfruit',119,29,1.6,0.4,'breakfast','vegan'),(32,'Breakfast cereal',267,49.7,12.4,3.4,'breakfast','vegan'),(33,'Broccoli',34,3.5,4.1,0.5,'lunch','vegan'),(34,'Brown Basmati Rice',131,28.7,3.3,1.1,'lunch','vegan'),(35,'Brown Trout',135,0,23.5,4.5,'lunch','pescatarian'),(36,'Brussels sprouts',32,4.2,3.1,0.4,'lunch','vegan'),(37,'Buckwheat',364,84.9,8.1,1.5,'breakfast','vegan'),(38,'Burger 85% lean beef',229,8.5,18.3,13.8,'lunch',''),(39,'Burger 99% lean beef',326,0.1,26.5,24.4,'lunch',''),(40,'Cabbage',17,2.3,1.5,0.2,'lunch','vegan'),(41,'Carp',112,0,17.5,4.7,'lunch','pescatarian'),(42,'Carrot juice',24,5.7,0.5,0.1,'lunch','vegan'),(43,'Carrots',30,6,0.7,0.5,'lunch','vegan'),(44,'Cashew fruit',33,6.8,0.9,0.4,'breakfast','vegan'),(45,'Cashew nuts',573,18.1,17.7,48.2,'lunch','vegan'),(46,'Cauliflower',29,3.5,1.9,0.9,'lunch','vegan'),(47,'Caviare',92,0,10.9,5.4,'lunch','pescatarian'),(48,'Celeriac',15,1.9,0.9,0.5,'lunch','vegan'),(49,'Celery',9,1.4,0.5,0.1,'lunch','vegan'),(50,'Chard',20,3.2,1.9,0.1,'lunch','vegan'),(51,'Cheddar Cheese 30% less fat',314,0.8,27.9,22.1,'lunch','vegetarian'),(52,'Cheese spread reduced fat',154,7.9,15,7.2,'lunch','vegetarian'),(53,'Cherries',58,13.4,1.1,0.4,'lunch','vegan'),(54,'Chestnuts',140,30.4,1.6,2.2,'lunch','vegan'),(55,'Chicken Breast',148,0,32,2.2,'lunch',''),(56,'Chicken Drumsticks',152,0,26.6,5.1,'lunch',''),(57,'Chicken Giblets',156,0,22.9,7.1,'lunch',''),(58,'Chicken leg quarter',176,0,25,8.4,'lunch',''),(59,'Chicken slices',114,2,23.2,1.5,'lunch',''),(60,'Chicken Thighs',180,0,25.6,8.6,'lunch',''),(61,'Chicken wings',274,4.1,27.4,16.6,'lunch',''),(62,'Chicken wings',164,0,26.9,6.3,'lunch',''),(63,'Chicory',7,2.1,0.6,0.3,'lunch','vegan'),(64,'Chilli Peppers ',20,0.7,2.9,0.6,'lunch','vegan'),(65,'Chilli sauce',40,7.3,1.3,0.8,'lunch','vegan'),(66,'Chinese stir fry',92,19.9,1.4,1.3,'lunch','vegan'),(67,'Chital',90,0,18.1,1.9,'lunch',''),(68,'Chives',27,1.9,3.3,0.7,'lunch','vegan'),(69,'Cho cho',17,3.7,0.7,0.1,'breakfast','vegan'),(70,'Chorizo',395,2.4,24,32.2,'breakfast',''),(71,'Ciabatta Bread',271,52,10.2,3.9,'breakfast','vegan'),(72,'Clementine',41,9.6,0.7,0.2,'breakfast','vegan'),(73,'Cocoa powder',312,11.5,18.5,21.7,'breakfast','vegan'),(74,'Coconut milk',22,4.9,0.3,0.3,'breakfast','vegan'),(75,'Cod fish',98,0,22.8,0.8,'dinner','pescatarian'),(76,'Cod Roe ',104,0,21.7,1.9,'dinner','pescatarian'),(77,'Cooked Couscous',178,37.5,7.2,1,'lunch','vegan'),(78,'Coriander leaves',18,1.2,2.1,0.5,'lunch','vegan'),(79,'Cottage Cheese reduced fat',68,3.3,10.6,1.5,'lunch','vegetarian'),(80,'Courgette',15,1.8,1.3,0.3,'lunch','vegan'),(81,'crackling Pork ',550,0,36.2,45,'dinner',''),(82,'Cranberries',15,3.4,0.4,0.1,'lunch','vegan'),(83,'Crayfish',67,0,14.9,0.8,'dinner','pescatarian'),(84,'Cucumber',14,1.2,1,0.6,'lunch','vegan'),(85,'Curly kale',26,1,2.7,1.3,'lunch','vegan'),(86,'Cuttlefish',71,0,16.1,0.7,'dinner','pescatarian'),(87,'Dab',74,0,15.7,1.2,'lunch','pescatarian'),(88,'Diced Pork ',203,0,36.3,6.4,'dinner',''),(89,'Diced Turkey Thighs',181,0,28.3,7.5,'dinner',''),(90,'Dill',25,0.9,3.7,0.8,'lunch','vegan'),(91,'Dried Apricots',188,43.4,4.8,0.7,'breakfast','vegan'),(92,'Dried Cole leaves',19,1.2,1.7,0.8,'lunch','vegan'),(93,'Dried Dates',235,58.7,2.4,0.6,'breakfast','vegan'),(94,'Dried mixed fruit',268,68.1,2.3,0.4,'breakfast','vegan'),(95,'Dried Pineapple ',303,75.7,3.3,0.7,'breakfast','vegan'),(96,'Dried Raisins',256,62.6,3,1,'breakfast','vegan'),(97,'Dried Thyme',276,45.3,9.1,7.4,'lunch','vegan'),(98,'Dry Turkey Skin',481,0,29.9,40.2,'lunch',''),(99,'Duck meat',195,0,25.3,10.4,'dinner',''),(100,'Easy Cook Brown Rice',157,35.3,3.2,1.3,'lunch','vegan'),(101,'Easy Cook Long Grain White Rice',146,34.7,3,0.4,'lunch','vegan'),(102,'Easy Cook White Rice',138,32.2,3.5,0.4,'lunch','vegan'),(103,'Eel meat',137,0,21.7,5.5,'lunch',''),(104,'Eggs',143,0,14.1,9.6,'breakfast','vegetarian'),(105,'Elderberries',35,7.4,0.7,0.5,'breakfast','vegan'),(106,'Escalope Veal',196,0,33.7,6.8,'lunch',''),(107,'Feijoa',47,10.3,0.9,0.5,'lunch','vegan'),(108,'Feta Cheese',250,1.5,15.6,20.2,'lunch','vegetarian'),(109,'Figs',43,9.5,1.3,0.3,'breakfast','vegan'),(110,'Fillet Steak',200,0,28.7,9.5,'dinner',''),(111,'Flank Beef',309,0,27.1,22.3,'lunch',''),(112,'Flounder',101,0,20.3,2.2,'lunch','pescatarian'),(113,'Flying fish',86,0,21,0.3,'dinner','pescatarian'),(114,'Fore-Rib Beef',300,0,29.1,20.4,'lunch',''),(115,'Fresh Thyme',95,15.1,3,2.5,'lunch','vegan'),(116,'Frozen Edemame Beans ',142,6.5,12.2,7.6,'lunch','vegan'),(117,'Fruit Fat Free Yoghurt',59,10.1,4.8,0.2,'breakfast','vegetarian'),(118,'Fruit Sorbet',97,24.8,0.2,0.3,'breakfast','vegan'),(119,'Gajjeralla',272,39.3,3.6,12.3,'lunch',''),(120,'Garam masala',379,45.2,15.6,15.1,'lunch',''),(121,'Garlic',98,16.3,7.9,0.6,'lunch','vegan'),(122,'Garlic mushrooms',134,0.5,1.2,14.1,'breakfast',''),(123,'Garlic powder',246,42.7,18.7,1.2,'lunch',''),(124,'Ginger',44,8.1,1.8,0.8,'breakfast','vegan'),(125,'Goose meat',301,0,27.5,21.2,'dinner',''),(126,'Gooseberries',40,9.2,0.7,0.3,'breakfast','vegan'),(127,'Grapefruit',24,4.9,0.6,0.4,'breakfast','vegan'),(128,'Grapes',64,15.8,0.7,0.2,'breakfast','vegan'),(129,'Green salad',13,1.6,1,0.4,'lunch','vegan'),(130,'Greengages',38,9.2,0.7,0.1,'breakfast','vegan'),(131,'Grenadillas',42,7.5,2.8,0.3,'breakfast','vegan'),(132,'Grilled Coley',105,0,27.2,1.4,'lunch','pescatarian'),(133,'Grilled salmon',239,0,24.6,15.6,'dinner','pescatarian'),(134,'Grilled Turbot',122,0,22.7,3.5,'lunch','pescatarian'),(135,'Grilled Turkey Breast',155,0,35,1.7,'dinner',''),(136,'Grouse meat',128,0,27.6,2,'dinner',''),(137,'Guava',24,4.5,0.7,0.5,'breakfast','vegan'),(138,'Haddock',98,0,23.9,0.3,'lunch','pescatarian'),(139,'Hake',113,0,22.2,2.7,'lunch','pescatarian'),(140,'Halibut',121,0,25.3,2.2,'lunch','pescatarian'),(141,'Halibut',154,1.1,24.7,5.7,'lunch','pescatarian'),(142,'Halloumi Cheese',313,1.7,23.9,23.5,'lunch','vegetarian'),(143,'Ham',107,1,18.4,3.3,'lunch',''),(144,'Ham gammon joint',204,0,23.3,12.3,'lunch',''),(145,'Ham gammon rashers',199,0,27.5,9.9,'lunch',''),(146,'Hare meat only',192,0,29.9,8,'dinner',''),(147,'Hazelnuts',650,6,14.1,63.5,'breakfast','vegan'),(148,'Herring',181,0,20.1,11.2,'lunch','pescatarian'),(149,'Herring Roe',91,0,16.8,2.6,'lunch','pescatarian'),(150,'Hilsa',262,0,21.8,19.4,'lunch','pescatarian'),(151,'Hoki',121,0,24.1,2.7,'lunch','pescatarian'),(152,'Honey',288,76.4,0.4,0,'lunch','vegan'),(153,'Honey and comb',281,74.4,0.6,4.6,'lunch','vegan'),(154,'Houmous',307,10.5,6.8,26.7,'breakfast','vegan'),(155,'Italian White Rice',138,32.2,3.2,0.5,'lunch','vegan'),(156,'Jackfish',108,0,21.7,2.4,'dinner','pescatarian'),(157,'Jackfruit',88,21.4,1.3,0.3,'breakfast','vegan'),(158,'Jam ',123,31.9,0.5,0.1,'breakfast','vegan'),(159,'Jambu fruit',55,12.4,0.7,0.3,'breakfast','vegan'),(160,'John Dory',89,0,19,1.4,'lunch','pescatarian'),(161,'Jujube',87,19.7,1.5,0.3,'breakfast','vegan'),(162,'Kalabasu',68,0,14.7,1,'lunch','pescatarian'),(163,'Katla',100,0,19.5,2.4,'lunch','pescatarian'),(164,'Kippers',245,0,21.7,17.6,'lunch','pescatarian'),(165,'Kiwi',44,8.6,0.8,0.9,'breakfast','vegan'),(166,'Kohl rabi',18,3.1,1.2,0.2,'lunch','vegan'),(167,'Kumquats',43,9.3,0.9,0.5,'breakfast','vegan'),(168,'Lamb best end neck cutlets',238,0,28.5,13.8,'lunch',''),(169,'Lamb Brain',126,0,11.6,8.8,'lunch',''),(170,'Lamb breast',273,0,26.7,18.5,'lunch',''),(171,'Lamb Heart',226,0,25.3,13.9,'lunch',''),(172,'Lamb Kidney ',91,0,17,2.6,'lunch',''),(173,'Lamb leg chops',221,0,28.3,12,'lunch',''),(174,'Lamb leg joint',210,0,30.8,9.6,'lunch',''),(175,'Lamb leg steaks',198,0,29.2,9,'dinner',''),(176,'Lamb loin chops',257,0,34.4,13.3,'lunch',''),(177,'Lamb loin joint',209,0,28.2,10.7,'lunch',''),(178,'Lamb mince',208,0,24.4,12.3,'lunch',''),(179,'Lamb neck fillet',284,0,27.9,19.1,'lunch',''),(180,'Lamb rack of lean',225,0,27.1,13,'lunch',''),(181,'Lamb shoulder',218,0,27.2,12.1,'lunch',''),(182,'Lamb shoulder joint',235,0,28.4,13.5,'lunch',''),(183,'Lamb Sweetbread',217,0,28.7,11.4,'lunch',''),(184,'Langoustine',86,0,19.7,0.8,'lunch','pescatarian'),(185,'Lemon sole',91,0,21.5,0.6,'lunch','pescatarian'),(186,'Lemons',19,3.2,1,0.3,'lunch','vegan'),(187,'Lentil soup canned',46,8.5,3.1,0.2,'lunch','vegan'),(188,'Lentils green and brown',92,14.5,7.8,0.7,'lunch','vegan'),(189,'Lettuce',11,1.4,1.2,0.1,'lunch','vegan'),(190,'Lime juice',9,1.6,0.4,0.1,'lunch','vegan'),(191,'Limes',6,0.6,0.5,0.2,'lunch','vegan'),(192,'Ling',82,0,18.8,0.7,'lunch','pescatarian'),(193,'Liver sausage',226,6,13.4,16.7,'lunch',''),(194,'Long Grain White Rice',131,31.1,2.8,0.4,'lunch','vegan'),(195,'Lychees',58,14.3,0.9,0.1,'breakfast','vegan'),(196,'Mackerel',283,0,20.3,22.4,'lunch','pescatarian'),(197,'Mango Chutney',189,48.3,0.7,0.1,'breakfast','vegan'),(198,'Mangoes',48,10.7,0.7,0.6,'breakfast','vegan'),(199,'Mashed Potatoes',93,15.9,1.8,2.8,'lunch','vegan'),(200,'Melon',24,5.5,0.5,0.1,'breakfast','vegan'),(201,'Microwaved potato',92,21.5,2.6,0.1,'dinner','vegan'),(202,'Mince Beef',130,0,27,5,'lunch',''),(203,'Mince Veal',205,0,26.3,11.1,'lunch',''),(204,'Mint',43,5.3,3.8,0.7,'breakfast','vegan'),(205,'Mixed Nuts',581,11.6,23.8,49.1,'lunch','vegan'),(206,'Mixed Vegetables',42,6.6,3.3,0.5,'lunch','vegan'),(207,'Monkfish',96,0,22.7,0.6,'dinner','pescatarian'),(208,'Mullet',150,0,25.7,5.2,'lunch','pescatarian'),(209,'Mushroom soup carton',48,4.9,1.5,2.7,'lunch','vegetarian'),(210,'Mushrooms',9,0.1,1.4,0.3,'breakfast','vegan'),(211,'Mussels',74,2.5,12.1,1.8,'lunch','pescatarian'),(212,'Naan Bread',285,50.2,7.8,7.3,'breakfast','vegan'),(213,'Nectarines',43,9.8,1,0.3,'lunch','vegan'),(214,'Okra',16,1.9,1.8,0.2,'lunch','vegan'),(215,'Onions',35,8,1,0.1,'lunch','vegan'),(216,'Oranges',36,8.2,0.8,0.2,'lunch','vegan'),(217,'Ox Heart',157,0,27.8,5.1,'lunch',''),(218,'Ox Kidney',138,0,24.5,4.4,'lunch',''),(219,'Ox Liver ',198,3.6,24.8,9.5,'lunch',''),(220,'Ox Tongue',242,0,19.4,18.3,'dinner',''),(221,'Oxtail',243,0,30.5,13.4,'dinner',''),(222,'Oysters',65,2.7,10.8,1.3,'lunch','pescatarian'),(223,'Pak choi',14,1.9,1.5,0.1,'lunch','vegan'),(224,'Pangasius',109,0,21.8,2.3,'lunch','pescatarian'),(225,'Papaya',44,9.5,0.7,0.6,'lunch','vegan'),(226,'Parmesan Cheese',415,0.9,36.2,29.7,'lunch','vegetarian'),(227,'Parrot fish',83,0,19.9,0.4,'dinner','pescatarian'),(228,'Parsley',34,2.7,3,1.3,'lunch','vegan'),(229,'Parsnip',66,14.7,1.2,0.7,'lunch','vegan'),(230,'Partridge',212,0,36.7,7.2,'dinner',''),(231,'Passion fruit',36,5.8,2.6,0.4,'breakfast','vegan'),(232,'Pasta fusili',146,32.9,4.8,0.4,'lunch','vegetarian'),(233,'Pasta white spaghetti',141,31.5,4.4,0.6,'lunch','vegetarian'),(234,'Pasta wholewheat spaghetti',134,27.5,5.2,1.1,'lunch','vegetarian'),(235,'Pastichio',150,17.2,7,6.3,'breakfast','vegan'),(236,'Peaches',33,7.6,1,0.1,'breakfast','vegan'),(237,'Peanut butter',607,13.1,22.8,51.8,'breakfast','vegan'),(238,'Peanuts',590,10.3,25.7,49.8,'breakfast','vegan'),(239,'Pears',43,10.9,0.3,0.1,'breakfast','vegan'),(240,'Peas canned in water',59,8,5.3,0.9,'lunch','vegan'),(241,'Pecan nuts',689,5.8,9.2,70.1,'lunch','vegan'),(242,'Peppermints',393,102.7,0.5,0.7,'lunch','vegan'),(243,'Pheasant',220,0,27.9,12,'dinner',''),(244,'Physalis',53,11.1,1.8,0.2,'breakfast','vegan'),(245,'Pickled Beetroot',28,5.6,1.2,0.2,'lunch','vegan'),(246,'Pickled Gherkins',14,2.6,0.9,0.1,'lunch','vegan'),(247,'Pig Heart',162,0,25.1,6.8,'lunch',''),(248,'Pig Kidney',153,0,24.4,6.1,'lunch',''),(249,'Pig Liver ',189,3.6,25.6,8.1,'lunch',''),(250,'Pigeon meat',187,0,29,7.9,'dinner',''),(251,'Pine nuts',688,4,14,68.6,'breakfast','vegan'),(252,'Pineapple',45,11.4,0.5,0.1,'breakfast','vegan'),(253,'Pink Salmon canned in brine',138,0,23.6,4.8,'lunch','pescatarian'),(254,'Pistachio nuts',601,8.2,17.9,55.4,'breakfast','vegan'),(255,'Pitta Bread',255,55.1,9.1,1.3,'breakfast','vegan'),(256,'Pizza base',290,57.5,7.8,4.8,'lunch','vegan'),(257,'Plaice ',99,0,21.3,1.6,'lunch','pescatarian'),(258,'Plain Fat Free Yoghurt',54,8.2,5.4,0.2,'lunch','vegetarian'),(259,'Plantain',112,28.5,0.8,0.2,'lunch','vegan'),(260,'Plums',25,5.9,0.5,0.1,'lunch','vegan'),(261,'Pns king ',102,0,23.5,0.9,'lunch','pescatarian'),(262,'Pollock',124,0,28.2,1.2,'lunch','pescatarian'),(263,'Pomegranate',51,11.8,1.3,0.2,'breakfast','vegan'),(264,'Pomelo',30,6.8,0.6,0.2,'breakfast','vegan'),(265,'Pomfret black',99,0,18.8,2.6,'lunch','pescatarian'),(266,'Pomfret white',92,0,18.3,2.1,'lunch','pescatarian'),(267,'Pork belly',320,0,27.4,23.4,'dinner',''),(268,'Pork Diced Kebabs',208,0,37.4,6.5,'dinner',''),(269,'Pork Fat',515,0,14.2,50.9,'dinner',''),(270,'Pork Fillet Medallions',161,0,35.9,1.9,'dinner',''),(271,'Pork Fillet Strips',168,0,35.8,2.7,'dinner',''),(272,'Pork Hand Shoulder',259,0,27.5,16.5,'dinner',''),(273,'Pork Leg Joint',261,0,29.6,15.9,'dinner',''),(274,'Pork Loin Chops',247,0,36.2,11.4,'dinner',''),(275,'Pork Loin Steaks',247,0,32.7,12.9,'dinner',''),(276,'Pork Mince',191,0,24.4,10.4,'dinner',''),(277,'Pork Sausages',160,10.7,16.2,6.1,'lunch',''),(278,'Pork scratchings',606,0.2,47.9,46,'dinner',''),(279,'Pork Shoulder Chops',213,0,30.5,10.1,'dinner',''),(280,'Pork Shoulder Joint',260,0,24.4,18,'dinner',''),(281,'Pork Shoulder Steaks',292,0,29.2,19.5,'dinner',''),(282,'Pork spare ribs',281,5.8,26.3,17.1,'dinner',''),(283,'Porridge Oats with skimed milk',84,12.1,4.6,2.3,'breakfast','vegetarian'),(284,'Porridge with water',47,8.8,1.4,1,'breakfast','vegan'),(285,'Potato chips',189,35.3,3.2,4.9,'lunch','vegan'),(286,'Prunes ',160,38.4,2.8,0.5,'breakfast','vegan'),(287,'Prunes semi-dried',149,36.5,2.3,0.3,'breakfast','vegan'),(288,'Pumpkin',13,2.2,0.7,0.2,'lunch','vegan'),(289,'Quiche',289,21.2,8.1,19.7,'lunch',''),(290,'Quinces',26,6.3,0.3,0.1,'breakfast','vegan'),(291,'Quinoa',309,55.7,13.8,5,'lunch','vegan'),(292,'Rabbit',114,0,21.2,3.2,'dinner',''),(293,'Raddiccio',14,1.7,1.4,0.2,'lunch','vegan'),(294,'Rainbow Trout',150,0,23.8,6.1,'lunch','pescatarian'),(295,'Rambutan',69,16.3,1,0.4,'lunch','vegan'),(296,'Rape leaves',37,4.8,3.8,0.3,'lunch','vegan'),(297,'Raspberries',25,5.1,0.8,0.3,'breakfast','vegan'),(298,'Red Cabbage',15,2.3,0.8,0.3,'lunch','vegan'),(299,'Red Kidney Beans',266,44.1,22.1,1.4,'lunch','vegan'),(300,'Red Pepper ',21,4.3,0.8,0.2,'lunch','vegan'),(301,'Red Radish',12,1.4,0.7,0.4,'lunch','vegan'),(302,'Red rice',129,28.2,3,1.2,'lunch','vegan'),(303,'Red Salmon canned in brine',160,0,23.5,7.3,'lunch','pescatarian'),(304,'Red Snapper',126,0,24.5,3.1,'lunch','pescatarian'),(305,'Redfish',98,0,18.4,2.7,'dinner','pescatarian'),(306,'Rhubarb',14,1.2,1,0.6,'lunch','vegan'),(307,'Roasted Chicken',177,0,27.3,7.5,'lunch',''),(308,'Roasted Chicken',141,0,25.8,4.2,'lunch',''),(309,'Roasted Turkey',177,0,29.4,6.6,'dinner',''),(310,'Rock Salmon',154,0,16.6,9.7,'dinner','pescatarian'),(311,'Rohu',79,0,16.6,1.4,'lunch','pescatarian'),(312,'Roulade',182,4.5,10.1,13.3,'lunch','vegetarian'),(313,'Rump Steak',203,0,29.5,9.4,'dinner',''),(314,'Salad',45,4.9,0.6,2.7,'lunch','vegan'),(315,'Salami',438,0.5,20.9,39.2,'lunch','pescatarian'),(316,'Salami snack',504,1.9,25.1,44,'lunch','pescatarian'),(317,'Salsify',23,8.6,1.1,0.4,'dinner','vegan'),(318,'Salted Popcorn',470,59.3,9,23.5,'lunch',''),(319,'Sapodilla',69,15.5,0.6,0.9,'breakfast','vegan'),(320,'Sardines',172,0,25.4,7.8,'lunch','pescatarian'),(321,'Sardines canned in olive oil',220,0,23.3,14.1,'lunch','pescatarian'),(322,'Scallops',118,3.4,23.2,1.4,'lunch','pescatarian'),(323,'Sea Bass',154,0,23.2,6.8,'lunch','pescatarian'),(324,'Sea Bream',96,0,17.5,2.9,'lunch','vegan'),(325,'Seafood selection',87,2.9,15.6,1.5,'lunch','pescatarian'),(326,'Seafood sticks',102,14.9,7.3,1.9,'lunch','pescatarian'),(327,'Seeded Bread',270,43.8,9.9,7.4,'breakfast','vegan'),(328,'Sheep Tongue',289,0,18.2,24,'dinner',''),(329,'Shish kebab',206,0,29,10,'dinner',''),(330,'Silverside Beef',247,0,31,13.7,'lunch',''),(331,'Sirloin Beef',233,0,29.8,12.6,'lunch',''),(332,'Sirloin Steak',216,0,25.1,12.8,'dinner',''),(333,'Skate',79,0,18.9,0.5,'lunch','pescatarian'),(334,'Skimmed milk',33,4.9,3.4,0.1,'breakfast','vegetarian'),(335,'Smoothies',49,12.2,0.5,0.1,'breakfast','vegan'),(336,'Sole',71,0,16.6,0.5,'lunch','pescatarian'),(337,'Soya Bean Tofu ',261,2,23.5,17.7,'lunch','vegan'),(338,'Soya Beans',370,15.8,35.9,18.6,'lunch','vegan'),(339,'Soya milk',26,0.5,2.4,1.6,'breakfast','vegan'),(340,'Spinach',21,0.5,3.1,0.8,'lunch','vegan'),(341,'Sprats',415,0,24.9,35,'lunch','pescatarian'),(342,'Spring greens',20,1.6,1.9,0.7,'lunch','vegan'),(343,'Spring onions',23,3,2,0.5,'lunch','vegan'),(344,'Squash Acron',56,12.6,1.1,0.1,'lunch','vegan'),(345,'Squash Butternut',39,8.4,1.4,0.2,'lunch','vegan'),(346,'Squid',81,1.2,15.4,1.7,'lunch','pescatarian'),(347,'Star fruit',32,7.3,0.5,0.3,'breakfast','vegan'),(348,'Stberries',30,6.1,0.6,0.5,'breakfast','vegan'),(349,'Steamed Catfish',119,0,21.4,3.7,'dinner','pescatarian'),(350,'Sultanas',275,69.4,2.7,0.4,'breakfast','vegan'),(351,'Sunflower seeds',602,19.3,20.5,49.2,'breakfast','vegan'),(352,'Swede',26,5.8,0.7,0.1,'lunch','vegan'),(353,'Swordfish',139,0,22.9,5.2,'dinner','pescatarian'),(354,'Tabouleh',119,17.2,2.6,4.6,'lunch','vegan'),(355,'Tahini paste',607,0.9,18.5,58.9,'lunch','vegan'),(356,'Tamarillos',28,4.7,2,0.3,'breakfast','vegan'),(357,'Tamarind',238,56.5,2.3,0.3,'lunch','vegan'),(358,'Tannia',107,24.5,1.3,0.4,'lunch','vegan'),(359,'Tapioca',359,95,0.4,0.1,'lunch','vegan'),(360,'Taramasalata',517,7.4,3.2,52.9,'lunch','pescatarian'),(361,'Taro leaves',19,1.4,2.4,0.5,'lunch','vegan'),(362,'Taro, steamed',99,24.5,1.3,0.2,'lunch','vegan'),(363,'Tarragon',49,6.3,3.4,1.1,'lunch','vegan'),(364,'Tartare sauce',299,17.9,1.3,24.6,'lunch','vegan'),(365,'Tempeh',166,6.4,20.7,6.4,'lunch','vegan'),(366,'Thai Rice',352,84.5,6.4,1.1,'lunch',''),(367,'Tigernuts',403,45.7,4.3,23.8,'breakfast','vegan'),(368,'Toasted Brown Bread',266,54,10.1,2.6,'breakfast','vegan'),(369,'Toasted Wholemeal Bread',255,49.2,11.2,2.9,'breakfast','vegan'),(370,'Tofu spread',208,2.4,4.4,20.1,'lunch','vegan'),(371,'Tomato Chutney',128,31,1.2,0.2,'lunch','vegan'),(372,'Tomato pasta sauce for bolognese',44,6.9,1.5,1.3,'lunch','vegan'),(373,'Tomato pasta sauce napoletana',65,6.5,1.5,3.8,'lunch','vegan'),(374,'Tomato puree',67,12.9,4.4,0.2,'lunch','vegan'),(375,'Tomatoes',14,3,0.5,0.1,'breakfast','vegan'),(376,'Tortilla',285,53.9,7.8,5.7,'lunch','vegan'),(377,'Tortilla chips fried in sunflower oil',504,60.8,7.2,27.4,'lunch','vegan'),(378,'Trail mix',432,37.2,9.1,28.5,'breakfast','vegan'),(379,'Tuna canned in brine',109,0,24.9,1,'lunch','pescatarian'),(380,'Tuna canned in sunflower oil',159,0,25.4,6.4,'lunch','pescatarian'),(381,'Turkey drumsticks',186,0,27.4,8.5,'dinner',''),(382,'Turkey Giblets',192,0,28.1,8.8,'lunch',''),(383,'Turkey Mince',176,0,28.6,6.8,'lunch',''),(384,'Turkey slices',114,1.2,23,1.9,'lunch',''),(385,'Turkey Strips',164,0,31,4.5,'lunch',''),(386,'Turnip',12,2,0.6,0.2,'lunch','vegan'),(387,'Twiglets',393,63.3,12.3,11.8,'lunch','vegan'),(388,'Tzatziki',76,3.4,3.4,5.5,'lunch','vegan'),(389,'Vegetable Brown Rice Risotto',136,17.3,4,6.2,'lunch','vegan'),(390,'Vegetable soup canned',39,7.4,1.4,0.6,'lunch','vegan'),(391,'Vegetarian Sausages',179,9.2,14.9,9.4,'lunch','vegetarian'),(392,'Venison',165,0,35.6,2.5,'lunch',''),(393,'Walnuts',295,1.4,6.3,29.4,'breakfast','vegan'),(394,'Water chestnuts',46,10.4,1.4,0.2,'lunch','vegan'),(395,'Wheat Bran',186,20.6,14.8,5.5,'lunch','vegan'),(396,'Wheatgerm Bread',220,39.5,11.1,3.1,'breakfast','vegan'),(397,'White Basmati Rice',117,26.5,2.8,0.7,'lunch','vegan'),(398,'White Cabbage',16,3.2,0.8,0.1,'lunch','vegan'),(399,'White Radish',15,2.9,0.8,0.1,'lunch','vegan'),(400,'Whiting',85,0,19.4,0.8,'lunch','pescatarian'),(401,'Wholegrain Brown Rice',132,29.2,3.6,0.9,'lunch','vegan'),(402,'Wholemeal Bread Rolls',244,46.1,10.4,3.3,'breakfast','vegan'),(403,'Wild Rice',145,31.7,5.3,0.6,'lunch','vegan'),(404,'Wild Salmon ',215,0,26.5,12.1,'dinner','pescatarian'),(405,'Yam',153,37.5,2.1,0.4,'lunch','vegan'),(406,'Yeast extract',180,3.5,40.7,0.4,'breakfast','vegan'),(407,'Yellow Pepper ',23,4.6,0.8,0.2,'lunch','vegan');
/*!40000 ALTER TABLE `Food` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Food_High`
--

DROP TABLE IF EXISTS `Food_High`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Food_High` (
  `food_high_id` int NOT NULL AUTO_INCREMENT,
  `food_id` int DEFAULT NULL,
  `high_type` text,
  PRIMARY KEY (`food_high_id`),
  KEY `food_id` (`food_id`),
  CONSTRAINT `food_high_ibfk_1` FOREIGN KEY (`food_id`) REFERENCES `Food` (`food_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Food_High`
--

LOCK TABLES `Food_High` WRITE;
/*!40000 ALTER TABLE `Food_High` DISABLE KEYS */;
INSERT INTO `Food_High` VALUES (1,10,'high carbs'),(2,12,'high carbs'),(3,13,'high carbs'),(4,15,'high carbs'),(5,18,'high carbs'),(6,26,'high carbs'),(7,31,'high carbs'),(8,32,'high carbs'),(9,34,'high carbs'),(10,37,'high carbs'),(11,54,'high carbs'),(12,71,'high carbs'),(13,77,'high carbs'),(14,91,'high carbs'),(15,93,'high carbs'),(16,94,'high carbs'),(17,95,'high carbs'),(18,96,'high carbs'),(19,97,'high carbs'),(20,100,'high carbs'),(21,101,'high carbs'),(22,102,'high carbs'),(23,118,'high carbs'),(24,119,'high carbs'),(25,120,'high carbs'),(26,123,'high carbs'),(27,152,'high carbs'),(28,153,'high carbs'),(29,155,'high carbs'),(30,157,'high carbs'),(31,158,'high carbs'),(32,194,'high carbs'),(33,197,'high carbs'),(34,201,'high carbs'),(35,212,'high carbs'),(36,232,'high carbs'),(37,233,'high carbs'),(38,234,'high carbs'),(39,242,'high carbs'),(40,255,'high carbs'),(41,256,'high carbs'),(42,259,'high carbs'),(43,285,'high carbs'),(44,286,'high carbs'),(45,287,'high carbs'),(46,289,'high carbs'),(47,291,'high carbs'),(48,299,'high carbs'),(49,302,'high carbs'),(50,318,'high carbs'),(51,327,'high carbs'),(52,350,'high carbs'),(53,357,'high carbs'),(54,358,'high carbs'),(55,359,'high carbs'),(56,362,'high carbs'),(57,366,'high carbs'),(58,367,'high carbs'),(59,368,'high carbs'),(60,369,'high carbs'),(61,371,'high carbs'),(62,376,'high carbs'),(63,377,'high carbs'),(64,378,'high carbs'),(65,387,'high carbs'),(66,395,'high carbs'),(67,396,'high carbs'),(68,397,'high carbs'),(69,401,'high carbs'),(70,402,'high carbs'),(71,403,'high carbs'),(72,405,'high carbs');
/*!40000 ALTER TABLE `Food_High` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Food_Preference`
--

DROP TABLE IF EXISTS `Food_Preference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Food_Preference` (
  `preference_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `food_id` int DEFAULT NULL,
  PRIMARY KEY (`preference_id`),
  KEY `user_id` (`user_id`),
  KEY `food_id` (`food_id`),
  CONSTRAINT `food_preference_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `food_preference_ibfk_2` FOREIGN KEY (`food_id`) REFERENCES `Food` (`food_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Food_Preference`
--

LOCK TABLES `Food_Preference` WRITE;
/*!40000 ALTER TABLE `Food_Preference` DISABLE KEYS */;
/*!40000 ALTER TABLE `Food_Preference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `age` int DEFAULT NULL,
  `weight` int DEFAULT NULL,
  `height` int DEFAULT NULL,
  `gender` tinyint(1) DEFAULT NULL,
  `activity_level` text,
  `goal` text,
  `diet` text,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `meal_variety` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-02 21:46:54
