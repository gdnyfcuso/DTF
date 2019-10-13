-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: invest
-- ------------------------------------------------------
-- Server version	5.7.20-log

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
-- Table structure for table `fund_info`
--

DROP TABLE IF EXISTS `fund_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fund_info` (
  `fund_code` varchar(255) NOT NULL COMMENT '基金代码',
  `fund_name` varchar(255) DEFAULT NULL COMMENT '基金全称',
  `fund_abbr_name` varchar(255) DEFAULT NULL COMMENT '基金简称',
  `fund_type` varchar(255) DEFAULT NULL COMMENT '基金类型',
  `issue_date` varchar(255) DEFAULT NULL COMMENT '发行日期',
  `establish_date` varchar(255) DEFAULT NULL COMMENT '成立日期',
  `establish_scale` varchar(255) DEFAULT NULL COMMENT '成立日期规模',
  `asset_value` varchar(255) DEFAULT NULL COMMENT '最新资产规模',
  `asset_value_date` varchar(255) DEFAULT NULL COMMENT '最新资产规模日期',
  `units` varchar(255) DEFAULT NULL COMMENT '最新份额规模',
  `units_date` varchar(255) DEFAULT NULL COMMENT '最新份额规模',
  `fund_manager` varchar(255) DEFAULT NULL COMMENT '基金管理人',
  `fund_trustee` varchar(255) DEFAULT NULL COMMENT '基金托管人',
  `funder` varchar(255) DEFAULT NULL COMMENT '基金经理人',
  `total_div` varchar(255) DEFAULT NULL COMMENT '成立来分红',
  `mgt_fee` varchar(255) DEFAULT NULL COMMENT '管理费率',
  `trust_fee` varchar(255) DEFAULT NULL COMMENT '托管费率',
  `sale_fee` varchar(255) DEFAULT NULL COMMENT '销售服务费率',
  `buy_fee` varchar(255) DEFAULT NULL COMMENT '最高认购费率',
  `buy_fee2` varchar(255) DEFAULT NULL COMMENT '最高申购费率',
  `benchmark` varchar(1000) DEFAULT NULL COMMENT '业绩比较基准',
  `underlying` varchar(500) DEFAULT NULL COMMENT '跟踪标的',
  `data_source` varchar(255) DEFAULT 'eastmoney' COMMENT '数据来源',
  `created_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `created_by` varchar(255) DEFAULT 'eastmoney' COMMENT '创建人',
  `updated_by` varchar(255) DEFAULT 'eastmoney' COMMENT '更新人',
  PRIMARY KEY (`fund_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='基金基本信息表';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-13 15:50:11
