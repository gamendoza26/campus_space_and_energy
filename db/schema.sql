-- schema.sql

-- Table: public.june11_june17_bostock.csv

-- DROP TABLE IF EXISTS public."june11_june17_bostock.csv";

CREATE TABLE IF NOT EXISTS public."june11_june17_bostock.csv"
(
    _time date,
    asa_code text COLLATE pg_catalog."default",
    ipaddr text COLLATE pg_catalog."default",
    macaddr text COLLATE pg_catalog."default",
    msgtype text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default",
    ssid text COLLATE pg_catalog."default",
    "user" text COLLATE pg_catalog."default"
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."june11_june17_bostock.csv"
    OWNER to sm997postgres;
