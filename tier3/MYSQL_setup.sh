mysql -h localhost -u root -p$MYSQL_PASS <<MY_QUERY
CREATE USER IF NOT EXISTS 'weather_storage'@'localhost' IDENTIFIED BY $USER_SQL_PASS;
CREATE DATABASE weather;
USE weather;

CREATE TABLE stations (
  code CHAR(3) NOT NULL,
  name VARCHAR(255),
  lat DOUBLE(20, 18),
  long DOUBLE(20, 18),
  CONSTRAINT station_id PRIMARY KEY (code)
)

CREATE TABLE weather_data (
  time TIMESTAMP NOT NULL,
  station_id CHAR(3) NOT NULL,
  -- OTHER DATA GOES WEATHER_API_KEY
  CONSTRAINT unique_entry PRIMARY KEY (time, station_id)
)

MY_QUERY
