#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname mean_prices <<-EOSQL

    CREATE USER api_user WITH PASSWORD 'api_password'; 

    CREATE DATABASE mean_prices;

EOSQL
