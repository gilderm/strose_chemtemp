import os

pg_db_username = os.getenv('APP_DBUSER','postgres')
pg_db_password = os.getenv('APP_DBPASSWORD','1postgres1')
pg_db_name     = os.getenv('APP_DBNAME','chem')
pg_db_hostname = os.getenv('APP_DBHOSTNAME','172.16.119.129')
pg_db_port     = os.getenv('APP_DBPORT','15432')

