CREATE_DB_TEST="DROP DATABASE IF EXISTS test; CREATE DATABASE test;"
CREATE_TABLE_TEST="DROP TABLE IF EXISTS test.test; CREATE TABLE test.test ( \
                  id int(9) AUTO_INCREMENT NOT NULL, \
                  PRIMARY KEY (id) \
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;";
