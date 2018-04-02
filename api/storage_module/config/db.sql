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