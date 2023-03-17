-- UDFs


-- Procedures
DELIMITER !
CREATE PROCEDURE add_to_order(username VARCHAR(20), password VARCHAR(20))
BEGIN
  DECLARE salt CHAR (8);

  SELECT make_salt(8) INTO salt;

  INSERT INTO user_info VALUES(
    new_username, salt, SHA2(CONCAT(password, salt), 256)
  );
END !
DELIMITER ;

-- Triggers
