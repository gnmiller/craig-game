DROP DATABASE IF EXISTS `craig-game`;
CREATE DATABASE IF NOT EXISTS `craig-game`;

USE `craig-game`;

SET default_storage_engine=InnoDB;

CREATE TABLE IF NOT EXISTS `guilds` (
		`guild_id` VARCHAR(64) NOT NULL UNIQUE,
		`guild_name` VARCHAR(65),
		`added` DATE DEFAULT (CURRENT_DATE),
		`uniq_id` INTEGER AUTO_INCREMENT,
		PRIMARY KEY (`uniq_id`) 
) Engine=InnoDB;

CREATE TABLE IF NOT EXISTS `characters` (
        `char_id` INTEGER AUTO_INCREMENT UNIQUE,
        `char_name` VARCHAR(32) NOT NULL,
        `class` VARCHAR(32) NOT NULL,
        `level` INTEGER ,
        `user_id` VARCHAR(32) NOT NULL,
        CONSTRAINT pk_characters PRIMARY KEY (`char_id`),
        INDEX uniq_name (`char_name`,`user_id`)
) Engine=InnoDB;

CREATE TABLE IF NOT EXISTS `exp` (
		`char_id` INTEGER AUTO_INCREMENT UNIQUE,
        `value` INTEGER,
        CONSTRAINT fk_exp FOREIGN KEY (`char_id`) REFERENCES `characters` (`char_id`),
        CONSTRAINT pk_exp PRIMARY KEY (`char_id`)
) Engine=InnoDB;

CREATE TABLE IF NOT EXISTS `equipment` (
		`char_id` INTEGER UNIQUE,
        `head` VARCHAR(32) DEFAULT NULL,
        `chest` VARCHAR(32) DEFAULT NULL,
        `arms` VARCHAR(32) DEFAULT NULL,
        `legs` VARCHAR(32) DEFAULT NULL,
        `hands` VARCHAR(32) DEFAULT NULL,
        `ring1` VARCHAR(32) DEFAULT NULL,
        `ring2` VARCHAR(32) DEFAULT NULL,
        `trinket` VARCHAR(32) DEFAULT NULL,
        `mh` VARCHAR(32) DEFAULT NULL,
        `oh` VARCHAR(32) DEFAULT NULL,
        CONSTRAINT fk_equip FOREIGN KEY (`char_id`) REFERENCES `characters` (`char_id`)
) Engine=InnoDB;

CREATE TABLE IF NOT EXISTS `items` (
        `item_id` INTEGER AUTO_INCREMENT UNIQUE,
        `item_name` VARCHAR(32),
        `item_slot` VARCHAR(32),
        CONSTRAINT pk_items PRIMARY KEY (`item_id`, `item_name`)
) Engine=InnoDB;

-- stats as a dict in the db?
CREATE TABLE IF NOT EXISTS `gear_armor` (
        `item_id` INTEGER UNIQUE,
        `item_slot` VARCHAR(32),
        `b_str` INTEGER DEFAULT 0,
        `b_int` INTEGER DEFAULT 0,
        `b_agi` INTEGER DEFAULT 0,
        `b_cha` INTEGER DEFAULT 0,
        `b_con` INTEGER DEFAULT 0,
        `b_luck` INTEGER DEFAULT 0,
        CONSTRAINT pk_gear_armor PRIMARY KEY (`item_id`),
        CONSTRAINT fk_gear_armor FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) Engine=InnoDB;

CREATE TABLE IF NOT EXISTS `gear_weapon` (
        `item_id` INTEGER UNIQUE,
        `item_slot` VARCHAR(32),
        `hands` VARCHAR(32),
        `b_str` INTEGER DEFAULT 0,
        `b_int` INTEGER DEFAULT 0,
        `b_agi` INTEGER DEFAULT 0,
        `b_cha` INTEGER DEFAULT 0,
        `b_con` INTEGER DEFAULT 0,
        `b_luck` INTEGER DEFAULT 0,
        CONSTRAINT pk_gear_weapon PRIMARY KEY (`item_id`),
        CONSTRAINT fk_gear_weapon FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) Engine=InnoDB;

CREATE TABLE IF NOT EXISTS `stats` (
        `char_id` INTEGER DEFAULT 0,
        `str` INTEGER DEFAULT 0,
        `int` INTEGER DEFAULT 0,
        `agi` INTEGER DEFAULT 0,
        `cha` INTEGER DEFAULT 0,
        `con` INTEGER DEFAULT 0,
        `luck` INTEGER DEFAULT 0,
        CONSTRAINT fk_stats FOREIGN KEY (`char_id`) REFERENCES `characters` (`char_id`),
        CONSTRAINT pk_stats PRIMARY KEY (`char_id`)
) Engine=InnoDB;