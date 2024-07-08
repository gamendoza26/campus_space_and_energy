#!/bin/bash

# Wait for PostgreSQL to start
until pg_isready -h pgdatabase -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Export table to CSV
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\COPY public.\"june11_june17_bostock.csv\" TO '/csv/june11_june17_bostock.csv' CSV HEADER;"
