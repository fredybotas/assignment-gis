FROM mdillon/postgis:11-alpine

ENV PDT_PASS=pdt_pass

COPY pdt_initdb.sh /docker-entrypoint-initdb.d

COPY db_dump.gz /docker-entrypoint-initdb.d
