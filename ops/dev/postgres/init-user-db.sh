#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER pypular;
    CREATE DATABASE pypular;
    GRANT ALL PRIVILEGES ON DATABASE pypular TO docker;
EOSQL