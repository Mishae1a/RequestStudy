CREATE TABLE `lj_transaction` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `city_code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '城市编码',
  `lj_id` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT 'lj_id',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '标题',
  `trade_time` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '交易时间',
  `trade_time_2` timestamp NULL DEFAULT NULL COMMENT '交易时间2',
  `total_price` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0.00' COMMENT '总价',
  `total_unit` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '总价单位',
  `unit_price` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0.00' COMMENT '单价',
  `unit_unit` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '单价单位',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '爬取状态 1todo 2done',
  `floor` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '所在楼层',
  `house_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '户型',
  `area` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '建筑面积',
  `real_araa` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '套内面积',
  `guapai_time` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '挂牌时间',
  `ownership` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '交易权属',
  `house_usage` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '房屋用途',
  `house_limit` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '房屋年限',
  `attr_detail` text COLLATE utf8mb4_unicode_ci COMMENT 'attr_detail',
  `trade_list` text COLLATE utf8mb4_unicode_ci COMMENT '交易记录',
  `plot` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '小区',
  `plot_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '小区id',
  `location` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT 'location',
  `location_2` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '高德location',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `x` decimal(10,5) NOT NULL DEFAULT '0.00000' COMMENT 'x',
  `y` decimal(10,5) NOT NULL DEFAULT '0.00000' COMMENT 'y',
  `distance_nk` decimal(10,2) unsigned NOT NULL DEFAULT '0.00',
  `distance_lgy` decimal(10,2) unsigned NOT NULL DEFAULT '0.00',
  `in_six_fence` tinyint(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `lj_id` (`lj_id`) USING BTREE,
  KEY `x` (`x`) USING BTREE,
  KEY `y` (`y`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `zjw_beijing` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `dt` varchar(180) NOT NULL DEFAULT '' COMMENT '日期',
  `net_number` varchar(255) NOT NULL DEFAULT '' COMMENT '网上签约套数',
  `net_area` varchar(255) NOT NULL DEFAULT '' COMMENT '网上签约面积',
  `residence_number` varchar(255) NOT NULL DEFAULT '' COMMENT '住宅签约套数',
  `residence_area` varchar(255) NOT NULL DEFAULT '' COMMENT '住宅签约面积',
  PRIMARY KEY (`id`),
  KEY `dt` (`dt`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 爬后处理
-- UPDATE lj_transaction SET trade_time_2=(CASE WHEN length(trade_time)=7 THEN concat(replace(trade_time, '.', '-'), '-01') ELSE replace(trade_time, '.', '-') END);
