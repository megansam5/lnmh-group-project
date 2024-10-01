DROP TABLE IF EXISTS recording;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS botanist;
DROP TABLE IF EXISTS location;

CREATE TABLE location (
    location_id SMALLINT IDENTITY(1,1),
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(100) NOT NULL,
    PRIMARY KEY (location_id)
);

CREATE TABLE botanist (
    botanist_id SMALLINT IDENTITY(1,1),
    botanist_name VARCHAR(100) UNIQUE NOT NULL,
    botanist_email VARCHAR(100),
    botanist_phone_no VARCHAR(100),
    PRIMARY KEY (botanist_id)
);

CREATE TABLE plant (
    plant_id SMALLINT UNIQUE NOT NULL,
    plant_name VARCHAR(100) UNIQUE NOT NULL,
    scientific_name VARCHAR(100) UNIQUE,
    location_id SMALLINT NOT NULL,
    botanist_id SMALLINT NOT NULL,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (botanist_id) REFERENCES botanist,
    FOREIGN KEY (location_id) REFERENCES location
);

CREATE TABLE recording (
    recording_id BIGINT IDENTITY(1,1),
    plant_id SMALLINT NOT NULL,
    recording_taken TIMESTAMP NOT NULL,
    last_watered TIMESTAMP,
    soil_moisture FLOAT,
    temperature FLOAT,
    PRIMARY KEY (recording_id),
    FOREIGN KEY (plant_id) REFERENCES plant
);
