DROP TABLE IF EXISTS recording;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS botanist;
DROP TABLE IF EXISTS location;

CREATE TABLE location (
    location_id SMALLINT UNIQUE NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(100) NOT NULL,
    PRIMARY KEY (location_id)
);

CREATE TABLE botanist (
    botanist_id SMALLINT UNIQUE NOT NULL,
    botanist_name VARCHAR(100) UNIQUE NOT NULL,
    botanist_email VARCHAR(100),
    botanist_phone_no VARCHAR(100),
    PRIMARY KEY (botanist_id)
);
n
CREATE TABLE plant (
    plant_id SMALLINT UNIQUE NOT NULL,
    plant_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(100) NOT NULL,
    image_url VARCHAR(100),
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

INSERT INTO location (location_id, latitude, longitude, city_name, country_code) VALUES
(1, -19.32556, -41.25528, 'Resplendor', 'BR'),
(2, 33.95015, -118.03917, 'South Whittier', 'US'),
(3, 7.65649, 4.92235, 'Efon-Alaaye', 'NG'),
(4, 13.70167, -89.10944, 'Ilopango', 'SV'),
(5, 22.88783, 84.13864, 'Jashpurnagar', 'IN'),
(6, 43.86682, -79.2663, 'Markham', 'CA'),
(7, 5.27247, -3.59625, 'Bonoua', 'CI'),
(8, 50.9803, 11.32903, 'Weimar', 'DE'),
(9, 43.50891, 16.43915, 'Split', 'HR'),
(10, 20.88953, -156.47432, 'Kahului', 'US'),
(11, 32.5007, -94.74049, 'Longview', 'US'),
(12, 49.68369, 8.61839, 'Bensheim', 'DE'),
(13, 29.65163, -82.32483, 'Gainesville', 'US'),
(14, 36.08497, 9.37082, 'Siliana', 'TN'),
(15, 40.93121, -73.89875, 'Yonkers', 'US'),
(16, -7.51611, 109.05389, 'Wangon', 'ID'),
(17, 51.30001, 13.10984, 'Oschatz', 'DE'),
(18, -21.44236, 27.46153, 'Tonota', 'BW'),
(19, 41.15612, 1.10687, 'Reus', 'ES'),
(20, -29.2975, -51.50361, 'Carlos Barbosa', 'BR'),
(21, 48.35693, 10.98461, 'Friedberg', 'DE'),
(22, 52.53048, 13.29371, 'Charlottenburg-Nord', 'DE'),
(23, 43.82634, 144.09638, 'Motomachi', 'JP'),
(24, 11.8659, 34.3869, 'Ar Ruseris', 'SD');

INSERT INTO botanist (botanist_id, botanist_name, botanist_email, botanist_phone_no) VALUES
(1, 'Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'),
(2, 'Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'),
(3, 'Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948');

INSERT INTO plant (plant_id, plant_name, scientific_name, image_url, location_id, botanist_id) VALUES
(0, 'Golden Pothos', 'Epipremnum Aureum', , 1, 1),
(1, 'Venus Flytrap', 'Dionaea Muscipula', , 2, 2),
(2, 'Corpse Flower', 'Amorphophallus Barteri', , 3, 1),
(3, 'Corpse Flower', 'Rafflesia Arnoldii', , 1, 3),
(4, 'Black Bat Flower', 'Tacca Chantrieri', , 4, 1),
(5, 'Pitcher Plant', 'Nepenthes Khasiana', , 5, 1),
(6, 'Wollemi Pine', 'Wollemia Nobilis', , 6, 3),
(8, 'False Bird of Paradise', 'Heliconia Schiedeana', , 7, 3),
(9, 'Cactus', 'Cactaceae', , 8, 2),
(10, 'Dragon Tree', 'Dracaena Draco', , 9, 2),
(11, 'Mexican Butterfly Weed', 'Asclepias Curassavica', , 10, 2),
(12, 'Angels Trumpet', 'Brugmansia X Candida', , 11, 3),
(13, 'Canna', 'Canna Striata', , 12, 3),
(14, 'Taro', 'Colocasia Esculenta', , 13, 2),
(15, 'Firecracker Bush', 'Cuphea David Verity', , 14, 2),
(16, 'Smoke Tree Spurge', 'Euphorbia Cotinifolia', , 15, 2),
(17, 'Sweet Potato', 'Ipomoea Batatas', , 16, 1),
(18, 'Variegated Tapioca', 'Manihot Esculenta Variegata', , 17, 1),
(19, 'Hardy Banana', 'Musa Basjoo', , 18, 2),
(20, 'Scarlet Sage', 'Salvia Splendens', , 19, 1),
(21, 'Flamingo Flower', 'Anthurium', , 20, 3),
(22, 'Bird of Paradise', 'Strelitzia Reginae', , 21, 2),
(23, 'Ti Plant', 'Cordyline Fruticosa', , 22, 3),
(24, 'Fig Tree', 'Ficus Carica', , 23, 1),
(25, 'Palm Tree', 'Arecaceae', , 24, 2);
