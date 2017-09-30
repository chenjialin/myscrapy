create database QianCheng;

#成都的python职位
CREATE TABLE `chengdu_python` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `position` varchar(100) DEFAULT NULL,
  `url` varchar(50) DEFAULT NULL,
  `company` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `salary` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#各个城市对应的编码
CREATE TABLE `area_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `area_code` varchar(50) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#全国各个城市的招聘
CREATE TABLE `city_position` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `position` varchar(100) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `company` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `salary` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;