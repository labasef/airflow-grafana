include .env
include .sql

start:
	docker-compose up -d --remove-orphans

maria:
	mysql --prompt="MariaDB (\u) [\d]>" -A -u root -proot -h127.0.0.1 -P 13306

metadb:
	psql postgresql://airflow:airflow@localhost:5444

create-db-test:
	mysql -A -u root -proot -h127.0.0.1 -P 13306 -e ${CREATE_DB_TEST}

stop:
	docker-compose down
