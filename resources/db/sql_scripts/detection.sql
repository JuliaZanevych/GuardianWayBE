CREATE TABLE Object (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

create  EXTENSION postgis;

CREATE TABLE public."location" (
    id SERIAL PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT,
    geo geography(POINT)
);

CREATE TABLE Detection (
  id SERIAL PRIMARY KEY,
  object_id INTEGER NOT NULL REFERENCES object(id),
  location_id INTEGER NOT NULL REFERENCES location(id),
  timestamp TIMESTAMP NOT NULL,
  density REAL NOT NULL
);

