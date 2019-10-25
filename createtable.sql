DROP TABLE IF EXISTS earthquakes;
CREATE TABLE earthquakes (
  quakedate date,
  quaketime time,
  latitude real,
  longitude real,
  quakedepth real,
  mag real,
  id text,
  place text,
  quaketype text
);