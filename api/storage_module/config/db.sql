CREATE DATABASE terramaapp;

CREATE TABLE public.locations
(
    id serial,
    description character varying(255),
    lat double precision,
    lng double precision,
    datetime date,
    photo text
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.locations
    OWNER to postgres;

INSERT INTO public.locations(
	id, description, lat, lng, datetime, photo)
	VALUES (?, ?, ?, ?, ?, ?);