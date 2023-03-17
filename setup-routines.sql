-- UDFs


-- Procedures
DELIMITER !
-- this will create a completely new order
-- item_ids is a string of a list of items like '1,2,5,7'   
CREATE PROCEDURE create_order(username VARCHAR(20), order_id BIGINT UNSIGNED, item_ids TEXT)
BEGIN
  DECLARE salt CHAR (8);

  SELECT make_salt(8) INTO salt;

  INSERT INTO user_info VALUES(
    new_username, salt, SHA2(CONCAT(password, salt), 256)
  );
END !
DELIMITER ;

-- Triggers
