include .env
include .sql

start:
	docker-compose up -d --remove-orphans
	make configure-airflow
	make configure-maria-connection
	make create-db-test

configure-airflow:
	docker exec airflow airflow users create --username ${AIRFLOW_USERNAME} --password ${AIRFLOW_PASSWORD} --role Admin --firstname basile --lastname labase --email basile@labase.dev

configure-maria-connection:
	docker exec airflow airflow connections add 'mysql_db' \
        --conn-host '${MYSQL_HOST}' \
        --conn-port '${MYSQL_PORT}' \
        --conn-type 'mysql' \
        --conn-login '${MYSQL_USER}' \
        --conn-password '${MYSQL_PASSWORD}'

create-db-test:
	mysql -A -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -h127.0.0.1 -P 13306 -e ${CREATE_DB_TEST}
	mysql -A -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -h127.0.0.1 -P 13306 -e ${CREATE_TABLE_TEST}


maria:
	mysql --prompt="MariaDB (\u) [\d]>" -A -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -h127.0.0.1 -P 13306

metadb:
	psql postgresql://airflow:airflow@localhost:5444

stop:
	docker-compose down
