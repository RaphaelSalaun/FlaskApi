#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname mean_prices <<-EOSQL
	CREATE SCHEMA mean_prices;

    CREATE TABLE mean_prices.files (
        id SERIAL PRIMARY KEY ,
        filename TEXT NOT NULL,
        created_date DATE NOT NULL DEFAULT CURRENT_DATE,
        status BOOLEAN NOT NULL
    );

    CREATE TABLE mean_prices.prices (
        id SERIAL PRIMARY KEY ,
        file_id INTEGER NOT NULL,
        gas_type TEXT NOT NULL,
        gas_price FLOAT NOT NULL,
        CONSTRAINT fk_file_id
        FOREIGN KEY(file_id) 
            REFERENCES mean_prices.files(id)
    );

    ALTER DATABASE mean_prices OWNER TO api_user;
    GRANT USAGE ON SCHEMA mean_prices TO api_user;
    GRANT ALL ON ALL TABLES IN SCHEMA mean_prices TO api_user ;
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA mean_prices TO api_user;
EOSQL