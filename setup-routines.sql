DROP FUNCTION IF EXISTS protein_in_item;
DROP FUNCTION IF EXISTS carbs_in_item;
DROP FUNCTION IF EXISTS fats_in_item;
DROP FUNCTION IF EXISTS sugars_in_item;
DROP FUNCTION IF EXISTS access_idx;
DROP PROCEDURE IF EXISTS create_order;

-- UDFs

DELIMITER !
CREATE FUNCTION protein_in_item (
    given_tem_id SERIAL
) RETURNS NUMERIC(6, 2) DETERMINISTIC
BEGIN
    DECLARE amount NUMERIC (6, 2);

    SELECT SUM(protein) INTO amount
    FROM (  SELECT protein
            FROM ingr_details NATURAL JOIN recipe
            WHERE item_id = given_tem_id ) AS temp;

    RETURN amount;
END !
DELIMITER ;

DELIMITER !
CREATE FUNCTION carbs_in_item (
    given_tem_id SERIAL
) RETURNS NUMERIC(6, 2) DETERMINISTIC
BEGIN
    DECLARE amount NUMERIC (6, 2);

    SELECT SUM(carbs) INTO amount
    FROM (  SELECT carbs
            FROM ingr_details NATURAL JOIN recipe
            WHERE item_id = given_tem_id) AS temp;

    RETURN amount;
END !
DELIMITER ;

DELIMITER !
CREATE FUNCTION fats_in_item (
    given_tem_id SERIAL
) RETURNS NUMERIC(6, 2) DETERMINISTIC
BEGIN
    DECLARE amount NUMERIC (6, 2);

    SELECT SUM(fats) INTO amount
    FROM (  SELECT fats
            FROM ingr_details NATURAL JOIN recipe
            WHERE item_id = given_tem_id) AS temp;

    RETURN amount;
END !
DELIMITER ;

DELIMITER !
CREATE FUNCTION sugars_in_item (
    given_tem_id SERIAL
) RETURNS NUMERIC(6, 2) DETERMINISTIC
BEGIN
    DECLARE amount NUMERIC (6, 2);

    SELECT SUM(sugars) INTO amount
    FROM (  SELECT sugars
            FROM ingr_details NATURAL JOIN recipe
            WHERE item_id = given_tem_id) AS temp;

    RETURN amount;
END !
DELIMITER ;

DELIMITER !
CREATE FUNCTION access_idx (
    set_str TEXT,
    which INT
) RETURNS NUMERIC(6, 2) DETERMINISTIC
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE st_search INT DEFAULT 1;
    DECLARE result TEXT;

    WHILE i < which DO
        SET i = i + 1;
        SET st_search = LOCATE('\,', set_str, st_search) + 1;
    END WHILE;

    IF LOCATE('\,', set_str, st_search) = 0 THEN
        SET result = SUBSTRING(set_str, st_search);
    ELSE
        SET result = SUBSTRING(set_str, st_search, LOCATE('\,', set_str, st_search)-st_search);
    END IF;

    RETURN CAST(result AS DECIMAL(6, 2));
END !
DELIMITER ;

-- Procedures
DELIMITER !

-- this will create a completely new order
-- item_ids is a string of a list of items like '1,2,5,7'   
-- it will create elements in orders_items for each item_id in string!!
CREATE PROCEDURE create_order(username VARCHAR(20), item_ids TEXT)
BEGIN
  DECLARE user_uid BIGINT UNSIGNED;
  DECLARE new_order_id BIGINT UNSIGNED;

  -- get uid for user from username
  SELECT uid FROM user WHERE user.username = username INTO user_uid;
  
  -- add to orders table, allow order_id to autogenerate
  INSERT INTO orders(uid, order_time) VALUES (user_uid, NOW());

  -- get the order_id that just generated
  SELECT order_id 
  FROM orders 
  WHERE order_time = (
    SELECT MAX(order_time) AS order_time FROM orders
  ) INTO new_order_id;

  -- the select statement will get the item ids that are included in the string
  -- it will insert a row for every set
  INSERT INTO orders_items (order_id, item_id) 
  SELECT new_order_id, item_id 
  FROM item 
  WHERE FIND_IN_SET(item_id, item_ids);
END !
DELIMITER ;

-- -- this will create a new menu item
-- -- item_ids is a string of a list of items like '1,2,5,7'   
-- -- it will create elements in orders_items for each item_id in string!!
-- CREATE PROCEDURE create_menu_item(name VARCHAR(40), price NUMERIC(6, 2), ingr_ids TEXT)
-- BEGIN
--   DECLARE user_uid BIGINT UNSIGNED;
--   DECLARE new_order_id BIGINT UNSIGNED;

--   -- get uid for user from username
--   SELECT uid FROM user WHERE user.username = username INTO user_uid;
  
--   -- add to orders table, allow order_id to autogenerate
--   INSERT INTO orders(uid, order_time) VALUES (user_uid, NOW());

--   -- get the order_id that just generated
--   SELECT order_id 
--   FROM orders 
--   WHERE order_time = (
--     SELECT MAX(order_time) AS order_time FROM orders
--   ) INTO new_order_id;

--   -- the select statement will get the item ids that are included in the string
--   -- it will insert a row for every set
--   INSERT INTO orders_items (order_id, item_id) 
--   SELECT new_order_id, item_id 
--   FROM item 
--   WHERE FIND_IN_SET(item_id, item_ids);
-- END !
-- DELIMITER ;

-- Triggers
