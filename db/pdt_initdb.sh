#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER pdt WITH ENCRYPTED PASSWORD '$PDT_PASS';
    CREATE USER michal WITH ENCRYPTED PASSWORD '$PDT_PASS';
    CREATE DATABASE pdt;
    GRANT ALL PRIVILEGES ON DATABASE pdt TO pdt;
EOSQL

gunzip -c /docker-entrypoint-initdb.d/db_dump.gz | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" pdt