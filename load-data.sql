CALL sp_add_user('pranav', 'ilovefood');
CALL sp_add_user('nisha', 'ilovesql');
CALL sp_add_user('john', 'ilovereddoor');



LOAD DATA LOCAL INFILE 'user.csv' INTO TABLE user
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'item.csv' INTO TABLE item
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS
(item_name, price_usd);

LOAD DATA LOCAL INFILE 'student.csv' INTO TABLE student
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'community_member.csv' INTO TABLE community_member
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS
(@id, @cnum, @edate, @vcode)
SET 
    uid = @id,
    credit_card_num = NULLIF(@cnum,''),
    expiration_date = NULLIF(@edate,''),
    verification_code = NULLIF(@vcode,'');


LOAD DATA LOCAL INFILE 'orders.csv' INTO TABLE orders
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'orders_items.csv' INTO TABLE orders_items
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;
