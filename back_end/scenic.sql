-- MySQL dump 10.13  Distrib 5.7.24, for osx11.1 (x86_64)
--
-- Host: localhost    Database: scenic
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add attraction',7,'add_attraction'),(26,'Can change attraction',7,'change_attraction'),(27,'Can delete attraction',7,'delete_attraction'),(28,'Can view attraction',7,'view_attraction'),(29,'Can add scenic',8,'add_scenic'),(30,'Can change scenic',8,'change_scenic'),(31,'Can delete scenic',8,'delete_scenic'),(32,'Can view scenic',8,'view_scenic'),(33,'Can add scenic spot',9,'add_scenicspot'),(34,'Can change scenic spot',9,'change_scenicspot'),(35,'Can delete scenic spot',9,'delete_scenicspot'),(36,'Can view scenic spot',9,'view_scenicspot'),(37,'Can add user',10,'add_user'),(38,'Can change user',10,'change_user'),(39,'Can delete user',10,'delete_user'),(40,'Can view user',10,'view_user'),(41,'Can add tour route',11,'add_tourroute'),(42,'Can change tour route',11,'change_tourroute'),(43,'Can delete tour route',11,'delete_tourroute'),(44,'Can view tour route',11,'view_tourroute'),(45,'Can add tour order',12,'add_tourorder'),(46,'Can change tour order',12,'change_tourorder'),(47,'Can delete tour order',12,'delete_tourorder'),(48,'Can view tour order',12,'view_tourorder'),(49,'Can add ticket',13,'add_ticket'),(50,'Can change ticket',13,'change_ticket'),(51,'Can delete ticket',13,'delete_ticket'),(52,'Can view ticket',13,'view_ticket'),(53,'Can add recommendation strategy',14,'add_recommendationstrategy'),(54,'Can change recommendation strategy',14,'change_recommendationstrategy'),(55,'Can delete recommendation strategy',14,'delete_recommendationstrategy'),(56,'Can view recommendation strategy',14,'view_recommendationstrategy'),(57,'Can add recommendation item',15,'add_recommendationitem'),(58,'Can change recommendation item',15,'change_recommendationitem'),(59,'Can delete recommendation item',15,'delete_recommendationitem'),(60,'Can view recommendation item',15,'view_recommendationitem'),(61,'Can add footprint',16,'add_footprint'),(62,'Can change footprint',16,'change_footprint'),(63,'Can delete footprint',16,'delete_footprint'),(64,'Can view footprint',16,'view_footprint'),(65,'Can add visitor',17,'add_visitor'),(66,'Can change visitor',17,'change_visitor'),(67,'Can delete visitor',17,'delete_visitor'),(68,'Can view visitor',17,'view_visitor'),(69,'Can add stay record',18,'add_stayrecord'),(70,'Can change stay record',18,'change_stayrecord'),(71,'Can delete stay record',18,'delete_stayrecord'),(72,'Can view stay record',18,'view_stayrecord');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'scenic','attraction'),(16,'scenic','footprint'),(15,'scenic','recommendationitem'),(14,'scenic','recommendationstrategy'),(8,'scenic','scenic'),(9,'scenic','scenicspot'),(18,'scenic','stayrecord'),(13,'scenic','ticket'),(12,'scenic','tourorder'),(11,'scenic','tourroute'),(10,'scenic','user'),(17,'scenic','visitor'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-02-14 03:52:21.882501'),(2,'auth','0001_initial','2024-02-14 03:52:22.008616'),(3,'admin','0001_initial','2024-02-14 03:52:22.035690'),(4,'admin','0002_logentry_remove_auto_add','2024-02-14 03:52:22.038463'),(5,'admin','0003_logentry_add_action_flag_choices','2024-02-14 03:52:22.041086'),(6,'contenttypes','0002_remove_content_type_name','2024-02-14 03:52:22.060071'),(7,'auth','0002_alter_permission_name_max_length','2024-02-14 03:52:22.069883'),(8,'auth','0003_alter_user_email_max_length','2024-02-14 03:52:22.077164'),(9,'auth','0004_alter_user_username_opts','2024-02-14 03:52:22.081292'),(10,'auth','0005_alter_user_last_login_null','2024-02-14 03:52:22.093982'),(11,'auth','0006_require_contenttypes_0002','2024-02-14 03:52:22.095154'),(12,'auth','0007_alter_validators_add_error_messages','2024-02-14 03:52:22.099489'),(13,'auth','0008_alter_user_username_max_length','2024-02-14 03:52:22.111852'),(14,'auth','0009_alter_user_last_name_max_length','2024-02-14 03:52:22.124943'),(15,'auth','0010_alter_group_name_max_length','2024-02-14 03:52:22.130863'),(16,'auth','0011_update_proxy_permissions','2024-02-14 03:52:22.134029'),(17,'auth','0012_alter_user_first_name_max_length','2024-02-14 03:52:22.149100'),(18,'scenic','0001_initial','2024-02-14 03:52:22.173122'),(19,'sessions','0001_initial','2024-02-14 03:52:22.180626'),(20,'scenic','0002_attraction_phone','2024-02-16 09:09:55.077937'),(21,'scenic','0003_alter_attraction_phone','2024-02-16 09:18:57.003854'),(22,'scenic','0004_auto_20240221_0526','2024-02-21 05:27:04.310771'),(23,'scenic','0005_auto_20240222_0314','2024-02-22 03:15:00.962450'),(24,'scenic','0006_alter_attraction_status','2024-02-22 03:27:10.520669'),(25,'scenic','0007_auto_20240223_0336','2024-02-23 03:36:06.365645'),(26,'scenic','0008_auto_20240223_0337','2024-02-23 03:37:31.673029'),(27,'scenic','0009_auto_20240224_0438','2024-02-24 04:38:48.271873'),(28,'scenic','0010_tourorder_tourroute','2024-02-25 09:49:46.911846'),(29,'scenic','0011_auto_20240225_0953','2024-02-25 09:53:22.461002'),(30,'scenic','0012_ticket','2024-02-26 03:09:35.092225'),(31,'scenic','0013_attraction_image','2024-03-19 11:44:54.016616'),(32,'scenic','0014_auto_20240328_0611','2024-03-28 06:11:48.130497'),(33,'scenic','0015_recommendationstrategy_status','2024-03-31 02:17:19.225621'),(34,'scenic','0016_scenic_image','2024-04-01 01:42:16.901915'),(35,'scenic','0017_auto_20240407_0728','2024-04-07 07:28:49.258340'),(36,'scenic','0018_remove_scenic_scale','2024-04-07 07:45:20.955366'),(37,'scenic','0019_scenic_scale','2024-04-07 07:46:02.998833'),(38,'scenic','0020_alter_footprint_check_in_time','2024-04-07 08:19:32.996599'),(39,'scenic','0021_auto_20240417_0552','2024-04-17 05:53:01.284477'),(40,'scenic','0022_stayrecord','2024-05-08 07:31:50.856905'),(41,'scenic','0023_tourroute_status','2024-05-12 02:27:18.199953'),(42,'scenic','0024_alter_attraction_description','2024-05-17 01:14:36.104782');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('b1pi9oyjeo2s46ecwk171689w66o7q60','eyJpbWFnZV9jb2RlIjoiU1hIS0ciLCJfc2Vzc2lvbl9leHBpcnkiOjYwfQ:1rfE0w:BweLKVhSm-qJfC-KH8YPnpemBoc61oTWQRJ9OK97R-E','2024-02-28 07:07:02.262729'),('cz8zn4wdskv8w9acwhx2hspxvcnkwl9p','eyJpbWFnZV9jb2RlIjoiUkVaRkciLCJfc2Vzc2lvbl9leHBpcnkiOjYwfQ:1re8CM:vAye6XSVrUBfhxtbT-z1-BZs75UdpSwBgNwpftKYwYU','2024-02-25 06:42:18.973172'),('exqz2waw58wqao694bi91an5w6v7droh','eyJpbWFnZV9jb2RlIjoiR01aQ1QiLCJfc2Vzc2lvbl9leHBpcnkiOjYwfQ:1re8Ah:IBc5ZBFT_SiuyOXFQqE0bZHP9WNNzR4uMjteSxF2j3U','2024-02-25 06:40:35.050098'),('uzen9lagqwzozoarc1txrec9z1a2dpvd','eyJpbWFnZV9jb2RlIjoiREpKUVYiLCJfc2Vzc2lvbl9leHBpcnkiOjYwfQ:1re8Eu:aSQEr1yJZRjnsg8-dodCLMfAep-qAt0BzhRvGpyAH94','2024-02-25 06:44:56.910915');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_attraction`
--

DROP TABLE IF EXISTS `scenic_attraction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_attraction` (
  `attraction_id` int NOT NULL AUTO_INCREMENT,
  `attraction_name` varchar(255) NOT NULL,
  `attraction_lng` double NOT NULL,
  `attraction_lat` double NOT NULL,
  `address` varchar(255) NOT NULL,
  `description` longtext,
  `category` smallint NOT NULL,
  `fee` double DEFAULT NULL,
  `open_time` time(6) NOT NULL,
  `close_time` time(6) NOT NULL,
  `flow_limit` int NOT NULL,
  `status` smallint NOT NULL,
  `count` int NOT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `scenic_id` int NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`attraction_id`),
  KEY `scenic_attraction_scenic_id_f0d8ff0f_fk_scenic_scenic_scenic_id` (`scenic_id`),
  CONSTRAINT `scenic_attraction_scenic_id_f0d8ff0f_fk_scenic_scenic_scenic_id` FOREIGN KEY (`scenic_id`) REFERENCES `scenic_scenic` (`scenic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_attraction`
--

LOCK TABLES `scenic_attraction` WRITE;
/*!40000 ALTER TABLE `scenic_attraction` DISABLE KEYS */;
INSERT INTO `scenic_attraction` VALUES (1,'三潭印月',120.145369,30.238886,'浙江省杭州市西湖区小瀛洲岛内','三潭印月，是浙江杭州西湖十景之一，被誉为“西湖第一胜境”。三潭印月是西湖中最大的岛屿，风景秀丽、景色清幽，尤三潭印月的景观享誉中外。',2,20,'08:00:00.000000','17:00:00.000000',10000,0,0,'',1,'attraction_images/三潭印月.jpg'),(2,'断桥残雪',120.151932,30.258878,'浙江省杭州市西湖区风景区白堤东端','断桥残雪是西湖上著名的景色，以冬雪时远观桥面若隐若现于湖面而称著。属于西湖十景之一。断桥残雪是欣赏西湖雪景之佳地，中国著名的民间传说《白蛇传》，为断桥景物增添了浪漫的色彩。',2,0,'00:00:00.000000','23:59:59.000000',20000,2,9000,'0571-87996663',1,'attraction_images/duanqiao.jpg'),(3,'苏堤春晓',120.138786,30.24173,'浙江省杭州市西湖区龙井路1号杭州西湖风景名胜区内','苏堤春晓，西湖十景之一，是指寒冬过后，苏堤报春的美妙景色。苏堤南起南屏山麓，北到栖霞岭下，全长近三公里，是北宋大诗人苏东坡任杭州知州时，疏浚西湖，利用挖出的葑泥构筑而成。后人为了纪念苏东坡治理西湖的功绩将它命名为苏堤。',2,0,'00:00:00.000000','23:59:59.000000',10000,1,800,'0',1,'attraction_images/苏堤春晓.jpg'),(4,'柳浪闻莺',120.156091,30.239813,'浙江省杭州市上城区南山路87号','柳浪闻莺是西湖十景之五，位于西湖东南岸，清波门处的大型公园。分友谊、闻莺、聚景、南园四个景区。柳丛衬托着紫楠、雪松、广玉兰、梅花等异木名花。',1,0,'00:00:00.000000','23:59:59.000000',25000,1,18923,'0571-87065684',1,'attraction_images/柳浪闻莺.jpg'),(5,'花港观鱼',120.139216,30.230203,'浙江省杭州市西湖区杨公堤10号','花港观鱼是由花、港、鱼为特色的风景点。西湖十景之一。地处苏堤南段西侧。全园分为红鱼池、牡丹园、花港、大草坪、密林地五个景区。与雷峰塔、净慈寺隔苏堤相望。',1,0,'00:00:00.000000','23:59:59.000000',10000,1,5348,'0571-87963033',1,'attraction_images/花港观鱼.jpg'),(6,'太子湾公园',120.1422,30.225491,'浙江省杭州市西湖区南山路5-1号','太子湾公园内有数千株日本东京樱，三月中旬盛开，灿若云霞，美不胜收。故名现为著名的婚庆公园与郁金香展地。',1,0,'00:00:00.000000','23:59:59.000000',30000,1,24395,'0',1,'attraction_images/太子湾.jpeg'),(7,'平湖秋月',120.146187,30.252092,'浙江省杭州市西湖区西湖风景区白堤西端','平湖秋月，西湖十景之一，是指：每当清秋气爽，西湖湖面平静如镜，皎洁的秋月当空，月光与湖水交相辉映，颇有“一色湖光万顷秋”之感，故题名“平湖秋月”。',1,0,'00:00:00.000000','23:59:59.000000',10000,1,3545,'0571-87977767',1,'attraction_images/平湖秋月.jpeg'),(8,'杭州苏东坡纪念馆',120.144031,30.228942,'浙江省杭州市西湖区南山路1号(苏堤南端)','苏东坡纪念馆由主楼展厅、碑廊、百坡亭、酹月轩等组成，粉墙黛瓦、玲珑可人。馆区曲径通幽，竹影婆娑，一尊苏东坡石雕像，立于苏堤入口左侧，衣袂飘然，昂首云外，仿佛还在与杭城百姓诉说着眷眷情愫。',3,0,'00:00:00.000000','23:59:59.000000',5000,2,4323,'0571-87179619',1,'attraction_images/苏东坡.jpeg'),(9,'杭州动物园',120.13294,30.21242,'浙江省杭州市虎跑路40号','杭州动物园饲养珍稀野生动物120种，近千头（只），园内设有大象馆、大熊猫馆、金鱼馆等20余个场馆，饲养展出金丝猴、长臂猿、黑猩猩、东北虎等各类珍稀野生动物。',4,20,'07:00:00.000000','17:00:00.000000',35000,1,24345,'0571-87970657',1,'attraction_images/zoo.jpeg'),(10,'杭州西湖观荷区',120.157132,30.258319,'浙江省杭州市拱墅区环城西路蝶来望湖宾馆西侧约170米','不管是第一次来西湖旅游的游客，还是老杭州人。一到夏天，就一定得去西湖走一趟。毕竟江南赏荷处，如有最佳，非杭州西湖莫属。',1,0,'00:00:00.000000','23:59:59.000000',10000,1,7543,'0571-87179539',1,'attraction_images/观荷区.jpg'),(11,'观鸟亭',120.067483,30.267037,'浙江省杭州市西湖区天目山路518号西溪国家湿地公园内(东北角)','西溪湿地观鸟亭生长着5000平米的喜林草,行走在这蓝盈盈的花海里,仿佛置身于莫奈油画，还可以近距离欣赏各种鸟类。',1,0,'08:00:00.000000','17:30:00.000000',2000,1,983,'0571-88106789',2,NULL),(12,'杭州湿地植物园',120.073463,30.272244,'浙江省杭州市西湖区天目山路518号西溪国家湿地公园(东北角)','湿地植物园是中国首个国家级湿地类植物园。园内总占地约55公顷，展示了西溪特色的基塘系统、河流、滩渚等生态多样性中的湿地植物。',1,0,'08:00:00.000000','17:30:00.000000',30000,0,0,'0571-89081133',2,NULL),(13,'朝天暮漾生态保育区',120.054371,30.274711,'浙江省杭州市西湖区天目山路518号西溪国家湿地公园内(北侧)','生态保育区内不设建筑、道路，以对池塘、湖沼、林地、植被等进行更好的保护培育，修复湿地功能，形成鱼禽鸟兽的良好栖息地。',1,0,'08:00:00.000000','17:30:00.000000',1000,1,0,'0',2,NULL),(14,'思母亭遗迹',120.050329,30.270414,'浙江省杭州市余杭区天目山路518号西溪国家湿地公园内(西北角)','思母亭遗迹位于五常街道西溪国家湿地公园三期五常港西侧。年代为明，类别为古遗址。2009年，思母亭遗迹被公布为杭州市市级文物保护单位。',2,0,'08:00:00.000000','17:30:00.000000',8000,1,4735,'0571-88106789',2,NULL),(15,'洪园',120.050933,30.262792,'浙江省杭州市余杭区五常大道龙舌嘴入口(西溪湿地西区)','洪园是西溪综合保护工程的\"收官之作\"，是一个集城市湿地、农耕湿地、文化湿地于一体的国家湿地公园，主打洪氏宗族文化，被誉为“城市水乡、洪昇故里”。',3,0,'08:00:00.000000','17:30:00.000000',10000,1,5395,'0571-89081177',2,NULL),(16,'欢乐水世界',119.115085,29.597954,'浙江省杭州市淳安县千岛湖镇珍珠半岛欢乐水世界','欢乐水世界以水上游乐项目为主，提供包括生态泳池、水上大闯关、摩托艇漂移、水上沙发、香蕉船冲浪、碰碰船、皮划艇等在内的20多个项目。',4,0,'00:00:00.000000','23:59:59.000000',18000,2,17324,'0571-65123456',3,NULL),(17,'千岛湖自然博物馆',119.019657,29.599639,'浙江省杭州市淳安县千岛湖镇梦姑路158号','千岛湖自然博物馆是一座集陈列、观赏、展览、征集、科研和科普教育于一体的现代化博物馆。',3,0,'00:00:00.000000','23:59:59.000000',20000,1,4345,'18969106669',3,NULL),(18,'温馨岛',119.032236,29.637179,'浙江省杭州市淳安县梦姑路348号千岛湖风景区(东北角)','温馨岛上的水上娱乐中心集现代水上娱乐之精华，空中有降落伞、水上飞机，水上有惊险刺激的冲浪舰、水上摩托和轻松休闲的自行车、情侣艇等等，水下可以潜水戏鱼。',1,0,'00:00:00.000000','23:59:59.000000',40000,1,23534,'0571-64831113',3,NULL),(19,'千岛湖观景平台',118.780607,29.526138,'浙江省杭州市淳安县淳开线千岛湖风景区内','千岛湖观景平台可以三面饱览千岛湖湖面，观千岛湖大桥全貌，俯瞅梅峰岛，是千岛湖最佳日落观景点。',1,0,'00:00:00.000000','23:59:59.000000',15000,1,13423,'0',3,NULL),(20,'鹿苑',119.989427,30.386839,'浙江省杭州市余杭区汽长线与祥凤线交叉口西100米大观山休憩区','鹿苑内有小鹿，人们可以近距离的接触小鹿，喂小鹿。',4,0,'09:00:00.000000','17:00:00.000000',3000,2,2200,'0571-85855300',4,NULL),(21,'茶语公园',120.018944,30.369537,'浙江省杭州市余杭区G104辅路与设计路交叉口正西方向790米左右','茶语公园内含各种青少年拓展游乐设施等，还设置有果园、宠物放羊去，溪水缠绕，环境幽雅宜人，更连接登山步道，是小镇有氧运动的理想场所。',1,0,'00:00:00.000000','23:59:59.000000',28000,1,23534,'null',4,NULL),(22,'良渚博物院',120.028044,30.377433,'浙江省杭州市余杭区美丽洲路1号','良渚博物院是由良渚文化博物馆升格而成的。截至2019年，良渚博物院有藏品数量3266件/套，有珍贵文物114件/套。',3,0,'09:00:00.000000','17:00:00.000000',26000,1,12323,'0571-88778900',4,NULL),(23,'西城墙遗址',119.982687,30.395006,'浙江省杭州市余杭区凤都路与104国道交叉口西北200米良渚古城遗址公园内城区域','爬上古城墙可以观赏整个园区的全貌，城墙周围布满了古代居民的宅地，这是良渚古城遗址公园的主要景观之一。',2,0,'09:00:00.000000','17:00:00.000000',10000,1,8932,'0571-85855300',4,NULL),(24,'悬空栈道',118.988201,30.03318,'浙江省杭州市临安区大明山风景区内','悬空栈道浮在云上，贴在山体绝壁之上，行走其上可以对大明山全景一览无遗，原先看不到的险峻之处一一呈现，婀娜多姿的明妃七峰亭亭玉立。',4,0,'00:00:00.000000','23:59:59.000000',2000,1,234,'0571-63709588',5,NULL),(25,'大明湖',118.990912,30.02528,'浙江省杭州市临安区清凉峰镇白果村大明山风景区内','大明湖湖畔有飞流直下的瀑布，壮如朵朵莲花的奇峰，碧波荡漾的湖泊，高僧坐禅的幽洞，朱元璋行军的古道，万千耸立的黑松，观看日出的高峰。',1,0,'00:00:00.000000','23:59:59.000000',30000,1,11232,'0571-63709588',5,NULL),(26,'万松岭滑雪场',118.994473,30.058999,'浙江省杭州市临安区上杭徽高速在白果口子下大明湖畔大明山风景区内','万松岭滑雪场目前拥有5千平方米的戏雪区和5万平方米的滑雪区，滑雪场雪道长落差大，还配置了初、中二级滑道。',4,200,'08:45:00.000000','18:00:00.000000',20000,1,2400,'13429637870',5,NULL),(27,'明妃七峰',118.982803,30.037116,'浙江省杭州市临安区昌化镇清凉峰镇白果村大明山风景区内(西侧)','明妃七峰的名字依次是广袖、湘愁、玉筝、羞月、霜冷、剑媚和落雁，都是非常诗化的名字，并且峰如其名，神态各异，风姿绰约，是大明山诸多峰林中有代表性的景观。',1,0,'00:00:00.000000','23:59:59.000000',25000,1,13422,'0571-63627888',5,NULL),(29,'曲苑风荷',120.135534,30.251113,'浙江省杭州市西湖区曙光路杭州西湖风景名胜区内',NULL,1,NULL,'00:00:00.000000','23:59:59.000000',10000,0,0,NULL,1,'attraction_images/曲苑风荷.jpeg'),(30,'宝石流霞',120.146078,30.26019,'浙江省杭州市西湖区昭庆寺里街22号','',1,0,'00:00:00.000000','23:59:59.000000',40000,0,0,'0571-87179603',1,''),(31,'茅家埠',120.125545,30.239471,'浙江省杭州市西湖区三台山杨公堤与龙井支路交叉口以北','',1,0,'00:00:00.000000','23:59:59.000000',4000,1,0,'0571-87179603',1,''),(32,'千岛湖森林氧吧',119.218036,29.586064,'浙江省杭州市淳安县千岛湖风景区704县道千岛湖镇淡竹王子山','',1,60,'08:00:00.000000','17:00:00.000000',50000,1,0,'0571-64832828',3,'');
/*!40000 ALTER TABLE `scenic_attraction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_footprint`
--

DROP TABLE IF EXISTS `scenic_footprint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_footprint` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `check_in_time` datetime(6) NOT NULL,
  `manual_check` tinyint(1) NOT NULL,
  `attraction_id` int NOT NULL,
  `scenic_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scenic_footprint_attraction_id_62ef84a1_fk_scenic_at` (`attraction_id`),
  KEY `scenic_footprint_scenic_id_f51bdfe7_fk_scenic_scenic_scenic_id` (`scenic_id`),
  KEY `scenic_footprint_user_id_3887e57c_fk_scenic_user_id` (`user_id`),
  CONSTRAINT `scenic_footprint_attraction_id_62ef84a1_fk_scenic_at` FOREIGN KEY (`attraction_id`) REFERENCES `scenic_attraction` (`attraction_id`),
  CONSTRAINT `scenic_footprint_scenic_id_f51bdfe7_fk_scenic_scenic_scenic_id` FOREIGN KEY (`scenic_id`) REFERENCES `scenic_scenic` (`scenic_id`),
  CONSTRAINT `scenic_footprint_user_id_3887e57c_fk_scenic_user_id` FOREIGN KEY (`user_id`) REFERENCES `scenic_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_footprint`
--

LOCK TABLES `scenic_footprint` WRITE;
/*!40000 ALTER TABLE `scenic_footprint` DISABLE KEYS */;
INSERT INTO `scenic_footprint` VALUES (1,'2024-04-07 12:00:00.000000',0,1,1,1),(2,'2024-04-07 13:00:00.000000',0,2,1,1),(3,'2024-04-07 14:00:00.000000',0,3,1,1),(4,'2024-04-07 15:00:00.000000',0,4,1,1),(5,'2024-04-08 11:00:00.000000',0,8,1,1),(6,'2024-05-05 12:37:54.356000',1,1,1,1),(7,'2024-05-05 12:45:40.475000',1,4,1,1),(8,'2024-05-05 12:46:11.606000',1,3,1,1),(9,'2024-05-05 12:48:17.657000',1,4,1,1),(10,'2024-05-05 13:18:16.595776',1,4,1,1),(11,'2024-05-05 13:21:01.927545',1,5,1,1),(12,'2024-05-05 13:27:51.192373',1,4,1,1),(13,'2024-05-05 13:31:53.103764',1,4,1,1),(14,'2024-05-01 13:35:21.000000',1,3,1,1),(15,'2024-05-02 13:35:21.000000',1,7,1,1),(16,'2024-05-05 06:04:34.000000',1,4,1,1),(17,'2024-05-20 08:56:02.000000',1,1,1,1),(18,'2024-05-30 12:09:05.000000',1,1,1,1);
/*!40000 ALTER TABLE `scenic_footprint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_recommendationitem`
--

DROP TABLE IF EXISTS `scenic_recommendationitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_recommendationitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order` int NOT NULL,
  `attraction_id` int NOT NULL,
  `strategy_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scenic_recommendatio_attraction_id_4884f1b3_fk_scenic_at` (`attraction_id`),
  KEY `scenic_recommendatio_strategy_id_bf4ec252_fk_scenic_re` (`strategy_id`),
  CONSTRAINT `scenic_recommendatio_attraction_id_4884f1b3_fk_scenic_at` FOREIGN KEY (`attraction_id`) REFERENCES `scenic_attraction` (`attraction_id`),
  CONSTRAINT `scenic_recommendatio_strategy_id_bf4ec252_fk_scenic_re` FOREIGN KEY (`strategy_id`) REFERENCES `scenic_recommendationstrategy` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_recommendationitem`
--

LOCK TABLES `scenic_recommendationitem` WRITE;
/*!40000 ALTER TABLE `scenic_recommendationitem` DISABLE KEYS */;
INSERT INTO `scenic_recommendationitem` VALUES (1,1,1,1),(2,2,2,1),(3,3,5,1),(4,4,10,1),(5,1,11,2),(6,2,15,2),(7,3,13,2),(8,4,14,2);
/*!40000 ALTER TABLE `scenic_recommendationitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_recommendationstrategy`
--

DROP TABLE IF EXISTS `scenic_recommendationstrategy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_recommendationstrategy` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `strategy_name` varchar(100) NOT NULL,
  `strategy_description` longtext,
  `strategy_type` smallint NOT NULL,
  `scenic_id` int NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scenic_recommendatio_scenic_id_0051e5c1_fk_scenic_sc` (`scenic_id`),
  CONSTRAINT `scenic_recommendatio_scenic_id_0051e5c1_fk_scenic_sc` FOREIGN KEY (`scenic_id`) REFERENCES `scenic_scenic` (`scenic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_recommendationstrategy`
--

LOCK TABLES `scenic_recommendationstrategy` WRITE;
/*!40000 ALTER TABLE `scenic_recommendationstrategy` DISABLE KEYS */;
INSERT INTO `scenic_recommendationstrategy` VALUES (1,'西湖景区自定义推荐',NULL,3,1,1),(2,'西溪湿地景区自定义推荐',NULL,3,2,1),(3,'西湖实时人数推荐策略',NULL,1,1,0),(4,'西湖热度推荐策略',NULL,2,1,0),(5,'千岛湖景区自定义推荐',NULL,3,3,1);
/*!40000 ALTER TABLE `scenic_recommendationstrategy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_scenic`
--

DROP TABLE IF EXISTS `scenic_scenic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_scenic` (
  `scenic_id` int NOT NULL,
  `scenic_name` varchar(255) NOT NULL,
  `scenic_lng` double NOT NULL,
  `scenic_lat` double NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `scale` int DEFAULT NULL,
  PRIMARY KEY (`scenic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_scenic`
--

LOCK TABLES `scenic_scenic` WRITE;
/*!40000 ALTER TABLE `scenic_scenic` DISABLE KEYS */;
INSERT INTO `scenic_scenic` VALUES (1,'西湖',120.146465,30.244667,'scenic_images/westlake.jpg',14),(2,'西溪湿地',120.064911,30.266962,'scenic_images/xixi.jpg',14),(3,'千岛湖',119.072218,29.558612,'scenic_images/qiandaohu.jpg',11),(4,'良渚古城',119.991218,30.390626,'scenic_images/liangzhu.jpg',15),(5,'大明山',118.997844,30.028484,'scenic_images/damingshan.jpg',14);
/*!40000 ALTER TABLE `scenic_scenic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_scenicspot`
--

DROP TABLE IF EXISTS `scenic_scenicspot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_scenicspot` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_scenicspot`
--

LOCK TABLES `scenic_scenicspot` WRITE;
/*!40000 ALTER TABLE `scenic_scenicspot` DISABLE KEYS */;
INSERT INTO `scenic_scenicspot` VALUES (1,'三潭印月','在西湖的瀛洲岛上，需要收费');
/*!40000 ALTER TABLE `scenic_scenicspot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_stayrecord`
--

DROP TABLE IF EXISTS `scenic_stayrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_stayrecord` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `check_in_time` datetime(6) NOT NULL,
  `attraction_id` int NOT NULL,
  `scenic_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scenic_stayrecord_attraction_id_57524666_fk_scenic_at` (`attraction_id`),
  KEY `scenic_stayrecord_scenic_id_8a6be0a0_fk_scenic_scenic_scenic_id` (`scenic_id`),
  KEY `scenic_stayrecord_user_id_5678e205_fk_scenic_user_id` (`user_id`),
  CONSTRAINT `scenic_stayrecord_attraction_id_57524666_fk_scenic_at` FOREIGN KEY (`attraction_id`) REFERENCES `scenic_attraction` (`attraction_id`),
  CONSTRAINT `scenic_stayrecord_scenic_id_8a6be0a0_fk_scenic_scenic_scenic_id` FOREIGN KEY (`scenic_id`) REFERENCES `scenic_scenic` (`scenic_id`),
  CONSTRAINT `scenic_stayrecord_user_id_5678e205_fk_scenic_user_id` FOREIGN KEY (`user_id`) REFERENCES `scenic_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_stayrecord`
--

LOCK TABLES `scenic_stayrecord` WRITE;
/*!40000 ALTER TABLE `scenic_stayrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `scenic_stayrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_ticket`
--

DROP TABLE IF EXISTS `scenic_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_ticket` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `ticket_count` int unsigned NOT NULL,
  `price` int NOT NULL,
  `status` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `attraction_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  `ticket_date` date DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `scenic_ticket_attraction_id_3dd4c23b_fk_scenic_at` (`attraction_id`),
  KEY `scenic_ticket_user_id_1fc95eb6_fk_scenic_user_id` (`user_id`),
  CONSTRAINT `scenic_ticket_attraction_id_3dd4c23b_fk_scenic_at` FOREIGN KEY (`attraction_id`) REFERENCES `scenic_attraction` (`attraction_id`),
  CONSTRAINT `scenic_ticket_user_id_1fc95eb6_fk_scenic_user_id` FOREIGN KEY (`user_id`) REFERENCES `scenic_user` (`id`),
  CONSTRAINT `scenic_ticket_chk_1` CHECK ((`ticket_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_ticket`
--

LOCK TABLES `scenic_ticket` WRITE;
/*!40000 ALTER TABLE `scenic_ticket` DISABLE KEYS */;
INSERT INTO `scenic_ticket` VALUES (11,1,20,3,'2024-04-20 06:48:12.363289',1,1,'2024-04-30'),(12,2,40,1,'2024-04-20 06:51:46.507057',1,1,'2024-04-24'),(13,1,20,2,'2024-04-20 06:54:19.021325',1,1,'2024-04-22'),(14,1,20,1,'2024-04-20 07:11:00.261437',9,1,'2024-04-22'),(15,1,20,0,'2024-04-27 07:11:00.261437',1,1,'2024-04-28');
/*!40000 ALTER TABLE `scenic_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_tourorder`
--

DROP TABLE IF EXISTS `scenic_tourorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_tourorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order` int NOT NULL,
  `attraction_id` int NOT NULL,
  `tour_route_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scenic_tourorder_attraction_id_8d77b278_fk_scenic_at` (`attraction_id`),
  KEY `scenic_tourorder_tour_route_id_e21e0af0_fk_scenic_tourroute_id` (`tour_route_id`),
  CONSTRAINT `scenic_tourorder_attraction_id_8d77b278_fk_scenic_at` FOREIGN KEY (`attraction_id`) REFERENCES `scenic_attraction` (`attraction_id`),
  CONSTRAINT `scenic_tourorder_tour_route_id_e21e0af0_fk_scenic_tourroute_id` FOREIGN KEY (`tour_route_id`) REFERENCES `scenic_tourroute` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_tourorder`
--

LOCK TABLES `scenic_tourorder` WRITE;
/*!40000 ALTER TABLE `scenic_tourorder` DISABLE KEYS */;
INSERT INTO `scenic_tourorder` VALUES (78,1,11,7),(79,2,12,7),(80,3,13,7),(81,1,1,4),(82,2,2,4),(83,3,3,4),(84,4,4,4),(85,5,5,4),(86,6,7,4),(87,1,1,6),(88,2,2,6),(91,1,4,1),(92,2,6,1),(93,3,3,1),(94,4,1,1),(95,5,5,1),(96,6,2,1);
/*!40000 ALTER TABLE `scenic_tourorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_tourroute`
--

DROP TABLE IF EXISTS `scenic_tourroute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_tourroute` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `scenic_id` int NOT NULL,
  `route_description` longtext,
  `route_name` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scenic_tourroute_scenic_id_8bc72f36_fk_scenic_scenic_scenic_id` (`scenic_id`),
  CONSTRAINT `scenic_tourroute_scenic_id_8bc72f36_fk_scenic_scenic_scenic_id` FOREIGN KEY (`scenic_id`) REFERENCES `scenic_scenic` (`scenic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_tourroute`
--

LOCK TABLES `scenic_tourroute` WRITE;
/*!40000 ALTER TABLE `scenic_tourroute` DISABLE KEYS */;
INSERT INTO `scenic_tourroute` VALUES (1,1,'适合春天的西湖游览路线','春日赏花线',1),(2,1,'test','经典红色游线',1),(3,1,'test','环湖惬意游',0),(4,1,'test','十景游路线',1),(5,1,'test','特种兵一日游路线',0),(6,2,'333test','222',0),(7,2,'111','xixi',1);
/*!40000 ALTER TABLE `scenic_tourroute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_user`
--

DROP TABLE IF EXISTS `scenic_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `phone` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_user`
--

LOCK TABLES `scenic_user` WRITE;
/*!40000 ALTER TABLE `scenic_user` DISABLE KEYS */;
INSERT INTO `scenic_user` VALUES (1,'棒打鲜陈','123456','18188886666'),(2,'别吃撑着了','789789','18966668888'),(3,'GregHan','19901031','13333338888'),(4,'meat','50d413b6631379605ec42281703ccfcb','14466677788'),(8,'wuhu','1122334455','13800138000'),(9,'wuhu','1122334455','13800138000'),(10,'xixi','11223344','13800138000'),(11,'please','guoguo','13800138000'),(12,'ww','xsxs','13800138000'),(13,'ww6','xsxsggg','13800138000'),(14,'汉堡包','123456','13800138000'),(15,'棒打鲜陈','12345','18188886666'),(16,'棒打鲜陈','123456','18188886666'),(17,'棒打鲜陈','12345','18188886666'),(18,'棒打鲜陈','12345','18188886666');
/*!40000 ALTER TABLE `scenic_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenic_visitor`
--

DROP TABLE IF EXISTS `scenic_visitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scenic_visitor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `idcard` varchar(18) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `ticket_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scenic_visitor_ticket_id_cb9dc0af_fk_scenic_ticket_ticket_id` (`ticket_id`),
  CONSTRAINT `scenic_visitor_ticket_id_cb9dc0af_fk_scenic_ticket_ticket_id` FOREIGN KEY (`ticket_id`) REFERENCES `scenic_ticket` (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenic_visitor`
--

LOCK TABLES `scenic_visitor` WRITE;
/*!40000 ALTER TABLE `scenic_visitor` DISABLE KEYS */;
INSERT INTO `scenic_visitor` VALUES (1,'rrr','222','222',11),(2,'www','111','111',12),(3,'eee','222','222',12),(4,'xxx','444','444',13),(5,'aaa','111','111',14);
/*!40000 ALTER TABLE `scenic_visitor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-10  9:30:45
