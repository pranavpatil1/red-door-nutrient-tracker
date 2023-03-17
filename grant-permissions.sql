-- issue with mysql on windows
CREATE USER 'appadmin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'adminpw';
CREATE USER 'appclient'@'localhost' IDENTIFIED WITH mysql_native_password BY 'clientpw';

-- Can add more users or refine permissions
GRANT ALL PRIVILEGES ON final.* TO 'appadmin'@'localhost';
GRANT SELECT ON final.* TO 'appclient'@'localhost';

FLUSH PRIVILEGES;