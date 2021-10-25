CREATE DATABASE IF NOT EXISTS weather;
USE weather;

CREATE TABLE stations (
  name VARCHAR(255) PRIMARY KEY,
  latitude DOUBLE,
  longitude DOUBLE
);

CREATE TABLE weather_data (
  time DATETIME NOT NULL,
  station_name CHAR(3) NOT NULL,
  temperature FLOAT,
  humidity FLOAT,
  heat_index FLOAT,
  dew_point FLOAT,
  wind_direction FLOAT,
  average_wind_speed FLOAT,
  warnings VARCHAR(255),
  PRIMARY KEY (station_name, time),
  FOREIGN KEY (station_name) REFERENCES stations (name)
);

INSERT INTO stations VALUES ("QUT Gardens Point", -27.477779504716224, 153.02954097170246);

CREATE USER IF NOT EXISTS 'weather_storage'@'localhost' IDENTIFIED BY 'Password123$';
GRANT INSERT, SELECT ON weather.weather_data TO 'weather_storage'@'localhost';
