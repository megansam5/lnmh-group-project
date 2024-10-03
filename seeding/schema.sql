DROP TABLE IF EXISTS alpha.recording;
DROP TABLE IF EXISTS alpha.plant;
DROP TABLE IF EXISTS alpha.botanist;
DROP TABLE IF EXISTS alpha.location;

CREATE TABLE alpha.location (
    location_id SMALLINT UNIQUE NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    city_name VARCHAR(180) NOT NULL,
    country_code VARCHAR(3) NOT NULL,
    PRIMARY KEY (location_id)
);

CREATE TABLE alpha.botanist (
    botanist_id SMALLINT UNIQUE NOT NULL,
    botanist_name VARCHAR(30) UNIQUE NOT NULL,
    botanist_email VARCHAR(50),
    botanist_phone_no VARCHAR(25),
    PRIMARY KEY (botanist_id)
);

CREATE TABLE alpha.plant (
    plant_id SMALLINT UNIQUE NOT NULL,
    plant_name VARCHAR(30) NOT NULL,
    scientific_name VARCHAR(50) NOT NULL,
    image_url VARCHAR(150),
    location_id SMALLINT NOT NULL,
    botanist_id SMALLINT NOT NULL,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (botanist_id) REFERENCES alpha.botanist(botanist_id),
    FOREIGN KEY (location_id) REFERENCES alpha.location(location_id)
);

CREATE TABLE alpha.recording (
    recording_id BIGINT IDENTITY(1,1),
    plant_id SMALLINT NOT NULL,
    recording_taken DATETIME2 NOT NULL,
    last_watered DATETIME2,
    soil_moisture FLOAT,
    temperature FLOAT,
    PRIMARY KEY (recording_id),
    FOREIGN KEY (plant_id) REFERENCES alpha.plant(plant_id)
);

INSERT INTO alpha.location (location_id, latitude, longitude, city_name, country_code) VALUES
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
(24, 11.8659, 34.3869, 'Ar Ruseris', 'SD'),
(25, 36.06386, 4.62744, 'El Achir', 'DZ'),
(26, 51.67822, 33.9162, 'Hlukhiv', 'UA'),
(27, 43.91452, -69.96533, 'Brunswick', 'US'),
(28, 34.75856, 136.13108, 'Ueno-ebisumachi', 'JP'),
(29, 30.75545, 20.22625, 'Ajdabiya', 'LY'),
(30, 23.29549, 113.82465, 'Licheng', 'CN'),
(31, 52.47774, 10.5511, 'Gifhorn', 'DE'),
(32, 28.92694, 78.23456, 'Bachhraon', 'IN'),
(33, -32.45242, -71.23106, 'La Ligua', 'CL'),
(34, 32.54044, -82.90375, 'Dublin', 'US'),
(35, 30.21121, 74.4818, 'Malaut', 'IN'),
(36, -6.8, 39.25, 'Magomeni', 'TZ'),
(37, 36.24624, 139.07204, 'Fujioka', 'JP'),
(38, 44.92801, 4.8951, 'Valence', 'FR'),
(39, 22.4711, 88.1453, 'Pujali', 'IN'),
(40, 41.57439, 24.71204, 'Smolyan', 'BG'),
(41, 20.22816, -103.5687, 'Zacoalco de Torres', 'MX'),
(42, -13.7804, 34.4587, 'Salima', 'MW'),
(43, 37.49223, 15.07041, 'Catania', 'IT'),
(44, 14.14989, 121.3152, 'Calauan', 'PH'),
(45, 17.94979, -94.91386, 'Acayucan', 'MX');

INSERT INTO alpha.botanist (botanist_id, botanist_name, botanist_email, botanist_phone_no) VALUES
(1, 'Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'),
(2, 'Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'),
(3, 'Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948');

INSERT INTO alpha.plant (plant_id, plant_name, scientific_name, image_url, location_id, botanist_id) VALUES
(0, 'Golden Pothos (a)', 'Epipremnum Aureum', 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/og/2560px-Epipremnum_aureum_31082012.jpg', 1, 1),
(1, 'Venus Flytrap', 'Dionaea Muscipula', 'https://perenual.com/storage/species_image/2498_dionaea_muscipula/og/2560px-Dionaea_muscipula2C_exhibition_in_Botanical_garden_Brno.jpg', 2, 2),
(2, 'Corpse Flower (a)', 'Amorphophallus Barteri', NULL, 3, 1),
(3, 'Corpse Flower (b)', 'Rafflesia Arnoldii', NULL, 1, 3),
(4, 'Black Bat Flower', 'Tacca Chantrieri', NULL, 4, 1),
(5, 'Pitcher Plant', 'Sarracenia Catesbaei', 'https://perenual.com/storage/species_image/7190_sarracenia_catesbaei/og/Sarracenia_x_catesbaei_x_psittacina_Kapturnica_2014-06-19_01.jpg', 5, 1),
(6, 'Wollemi Pine', 'Wollemia Nobilis', 'https://perenual.com/storage/species_image/8360_wollemia_nobilis/og/30129534108_43db758803_b.jpg', 6, 3),
(8, 'False Bird of Paradise', 'Heliconia Schiedeana ''Fire and Ice''', 'https://perenual.com/storage/species_image/3404_heliconia_schiedeana_fire_and_ice/og/52233116449_9b56243a59_b.jpg', 7, 3),
(9, 'Rose Cactus', 'Pereskia Grandifolia', 'https://perenual.com/storage/species_image/5809_pereskia_grandifolia/og/27487227123_a9b4d90e13_b.jpg', 8, 2),
(10, 'Dragontree', 'Dracaena Marginata', 'https://perenual.com/storage/species_image/2531_dracaena_marginata/og/24448909183_1a82d61ed5_b.jpg', 9, 2),
(11, 'Blood Flower', 'Asclepias Curassavica', 'https://perenual.com/storage/species_image/1007_asclepias_curassavica/og/51757177616_7ca0baaa87_b.jpg', 10, 2),
(12, 'Angel''s Trumpet', 'Brugmansia Candida', 'https://perenual.com/storage/species_image/1344_brugmansia_candida/og/4934191189_e7aece5acf_b.jpg', 11, 3),
(13, 'Canna', 'Canna ''Striata''', 'https://perenual.com/storage/species_image/1591_canna_striata/og/1536px-Canna_27Striata27_Paciorecznik_2019-09-15_03.jpg', 12, 3),
(14, 'Taro', 'Colocasia Esculenta', 'https://perenual.com/storage/species_image/2015_colocasia_esculenta/og/24325097844_14719030a3_b.jpg', 13, 2),
(15, 'Cuphea', 'Cuphea ''David Verity''', 'https://perenual.com/storage/species_image/2258_cuphea_david_verity/og/51854325106_33ed9ec628_b.jpg', 14, 2),
(16, 'Mexican Shrubby Spurge', 'Euphorbia Cotinifolia', 'https://perenual.com/storage/species_image/2868_euphorbia_cotinifolia/og/51952243235_061102bd05_b.jpg', 15, 2),
(17, 'Sweet Potato', 'Ipomoea Batatas', 'https://perenual.com/storage/species_image/4302_ipomoea_batatas/og/52457532874_163690b241_b.jpg', 16, 1),
(18, 'Bitter Cassava', 'Manihot Esculenta ''Variegata''', 'https://perenual.com/storage/species_image/5157_manihot_esculenta_variegata/og/14072622071_677ed41bbb_b.jpg', 17, 1),
(19, 'Japanese Banana', 'Musa Basjoo', 'https://perenual.com/storage/species_image/5282_musa_basjoo/og/49639151686_0ae07c39dd_b.jpg', 18, 2),
(20, 'Scarlet Sage', 'Salvia Splendens', 'https://perenual.com/storage/species_image/7126_salvia_splendens/og/52595771121_dbe8e86849_b.jpg', 19, 1),
(21, 'Anthurium', 'Anthurium Andraeanum', 'https://perenual.com/storage/species_image/855_anthurium_andraeanum/og/49388458462_0ef650db39_b.jpg', 20, 3),
(22, 'False Bird of Paradise', 'Heliconia Schiedeana ''Fire and Ice''', 'https://perenual.com/storage/species_image/3404_heliconia_schiedeana_fire_and_ice/og/52233116449_9b56243a59_b.jpg', 21, 2),
(23, 'Cabbage Tree', 'Cordyline Fruticosa', 'https://perenual.com/storage/species_image/2045_cordyline_fruticosa/og/2560px-Cordyline_fruticosa_Rubra_1.jpg', 22, 3),
(24, 'Common Fig', 'Ficus Carica', 'https://perenual.com/storage/species_image/288_ficus_carica/og/52377169610_b7a247a378_b.jpg', 23, 1),
(25, 'Palm Tree', 'Arecaceae', NULL, 24, 2),
(26, 'Dumb Cane', 'Dieffenbachia Seguine', 'https://perenual.com/storage/species_image/2468_dieffenbachia_seguine/og/24449059743_2aee995991_b.jpg', 25, 1),
(27, 'Peace Lily', 'Spathiphyllum', 'https://perenual.com/storage/species_image/7463_spathiphyllum_group/og/b4cfd76ce36d77ea460b3635517a73aab86fef0c.jpg', 26, 1),
(28, 'Croton', 'Codiaeum variegatum', 'https://perenual.com/storage/species_image/1999_codiaeum_variegatum/og/29041866364_2c535b2297_b.jpg', 27, 1),
(29, 'Aloe', 'Aloe Vera', 'https://perenual.com/storage/species_image/728_aloe_vera/og/52619084582_6ebcfe6a74_b.jpg', 28, 2),
(30, 'Indian Rubber Plant', 'Ficus Elastica', 'https://perenual.com/storage/species_image/2961_ficus_elastica/og/533092219_8da73ba0d2_b.jpg', 29, 1),
(31, 'Viper''s Bowstring Hemp', 'Sansevieria Trifasciata', 'https://perenual.com/storage/species_image/7171_sansevieria_trifasciata/og/36416803474_81e6bd3f2e_b.jpg', 30, 2),
(32, 'Vilevine', 'Philodendron Hederaceum', 'https://perenual.com/storage/species_image/5869_philodendron_hederaceum/og/Philodendron_hederaceum_var._kirkbridei_Leaves.jpg', 31, 2),
(33, 'Umbrella Plant', 'Schefflera Arboricola', 'https://perenual.com/storage/species_image/7245_schefflera_arboricola/og/50892679962_787651a1ea_b.jpg', 32, 1),
(34, 'Philippine Evergreen', 'Aglaonema Commutatum', 'https://perenual.com/storage/species_image/625_aglaonema_commutatum/og/24798632751_3a039ecbc6_b.jpg', 19, 2),
(35, 'Swiss Cheese Plant', 'Monstera Deliciosa', 'https://perenual.com/storage/species_image/5257_monstera_deliciosa/og/4630938853_623dc33137_b.jpg', 33, 1),
(36, 'Bat Plant', 'Tacca Integrifolia', 'https://perenual.com/storage/species_image/7680_tacca_integrifolia/og/e8ff33915f6f1d88b3c0088c9d8db50d5062d3e9.jpg', 34, 2),
(37, 'Butterfly Orchid', 'Psychopsis Papilio', NULL, 35, 3),
(38, 'African Violet', 'Saintpaulia Ionantha', 'https://perenual.com/storage/species_image/7030_saintpaulia_ionantha/og/46232918414_09d5aca9c4_b.jpg', 36, 2),
(39, 'Lance Leaf Blanket Flower', 'Gaillardia Aestivalis', 'https://perenual.com/storage/species_image/3060_gaillardia_aestivalis/og/park_flowers_blue_sunset_red_wild_hairy_sun-400538.jpg', 37, 1),
(40, 'Amaryllis', 'Hippeastrum', 'https://perenual.com/storage/species_image/3828_hippeastrum_group/og/amaryllis-flowers-christmas-christmas-flower.jpg', 38, 3),
(41, 'Angel Wings', 'Caladium Bicolor', 'https://perenual.com/storage/species_image/1457_caladium_bicolor/og/25575875658_d782fb76f1_b.jpg', 39, 1),
(42, 'Spider Plant', 'Chlorophytum Comosum ''Vittatum''', 'https://perenual.com/storage/species_image/1847_chlorophytum_comosum_vittatum/og/2560px-Chlorophytum_comosum_27Vittatum27_kz02.jpg', 40, 1),
(44, 'Norfolk Island Pine', 'Araucaria Heterophylla', 'https://perenual.com/storage/species_image/917_araucaria_heterophylla/og/49833684212_2aff9d7b3c_b.jpg', 41, 2),
(45, 'Begonia', 'Begonia ''Art Hodes''', NULL, 2, 2),
(46, 'Showy Medinilla', 'Medinilla Magnifica', 'https://perenual.com/storage/species_image/5180_medinilla_magnifica/og/52021835452_2e9d0bef62_b.jpg', 42, 3),
(47, 'Powder Puff Tree', 'Calliandra Haematocephala', 'https://perenual.com/storage/species_image/1477_calliandra_haematocephala/og/52063600268_834ebc0538_b.jpg', 43, 3),
(48, 'ZZ Plant', 'Zamioculcas Zamiifolia', 'https://perenual.com/storage/species_image/8386_zamioculcas_zamiifolia/og/24891577155_64934d420e_b.jpg', 44, 1),
(49, 'Jade Plant', 'Crassula Ovata', 'https://perenual.com/storage/species_image/2193_crassula_ovata/og/33253726791_980c738a1e_b.jpg', 45, 3),
(50, 'Golden Pothos (b)', 'Epipremnum Aureum', 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/og/2560px-Epipremnum_aureum_31082012.jpg', 1, 1);