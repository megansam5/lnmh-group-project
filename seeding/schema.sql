DROP TABLE IF EXISTS recording;
DROP TABLE IF EXISTS botanist;
DROP TABLE IF EXISTS plant;

CREATE TABLE plant (
    plant_id SMALLINT UNIQUE NOT NULL,
    plant_name VARCHAR(100) UNIQUE NOT NULL,
    scientific_name VARCHAR(100) UNIQUE,
    location_town VARCHAR(100),
    location_city VARCHAR(100),
    PRIMARY KEY (plant_id)
);


CREATE TABLE botanist (
    botanist_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    botanist_name VARCHAR(100) UNIQUE NOT NULL,
    botanist_email VARCHAR(100),
    botanist_phone_no VARCHAR(100)
);

CREATE TABLE recording (
    recording_id BIGINT GENERATED ALWAYS AS IDENTITY,
    botanist_id SMALLINT NOT NULL,
    plant_id SMALLINT NOT NULL,
    recording_taken TIMESTAMP NOT NULL,
    soil_moisture FLOAT,
    temperature FLOAT,
    FOREIGN KEY (botanist_id) REFERENCES botanist,
    FOREIGN KEY (plant_id) REFERENCES plant
);