CREATE DATABASE terramaapp;

CREATE TABLE public.locations
(
    id serial,
    description character varying(255),
    lat double precision,
    lng double precision,
    datetime date,
    photo_b64 text,
    picture character varying(255),
    CONSTRAINT pk_locations_id PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.locations
    OWNER to postgres;

-- Change table to create a new geometry column using srid=4326

CREATE EXTENSION postgis;

SELECT AddGeometryColumn ('public','locations','points',4326,'POINT',2);