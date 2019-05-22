-- CREATE DATABASE terramaapp;

CREATE EXTENSION postgis;

CREATE TABLE public.locations
(
    id serial,
    description character varying(255) COLLATE pg_catalog."default",
    lat double precision,
    lng double precision,
    picture character varying(255) COLLATE pg_catalog."default",
    datetime timestamp with time zone,
    points geometry(Point,4326),
    CONSTRAINT pk_locations_id PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

-- ALTER TABLE public.locations OWNER to postgres;
