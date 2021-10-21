
CREATE USER IF NOT EXISTS 'weather_storage'@'localhost' IDENTIFIED BY $USER_SQL_PASS;
CREATE DATABASE weather;
USE weather;

CREATE TABLE stations (
  name VARCHAR(255) PRIMARY KEY,
  lat DOUBLE(20, 18),
  long DOUBLE(20, 18),
)

CREATE TABLE weather_data (
  time TIMESTAMP NOT NULL,
  station_name CHAR(3) NOT NULL,
  temperature DECIMAL(3, 1),
  humidity FLOAT,
  heat_index FLOAT,
  dew_point FLOAT,
  wind_direction FLOAT,
  average_wind_speed FLOAT,
  wind_gust FLOAT,
  warnings VARCHAR(255),
  PRIMARY KEY (station_name, time)
  FOREIGN KEY (station_name) REFERENCES stations (station_id)
)
