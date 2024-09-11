
CREATE TABLE default_db.addresses (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `first_line` varchar(255),
  `secondary_line` varchar(255),
  `hash` varchar(255),
  PRIMARY KEY (`id`)
);
INSERT INTO default_db.addresses VALUES ('1', "это улица", "это дом","");
UPDATE default_db.addresses SET `hash` = MD5(CONCAT(`id`,`first_line`,`secondary_line`)) WHERE `id`=1;
