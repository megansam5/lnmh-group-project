# LMNH Botanical Garden Project

## Overview

The Liverpool Natural History Museum (LMNH has recently opened a botanical garden wing that houses a variety of plants from around the world. Each plant has a corresponding sensor that monitors the health of the plant and uploads to an API endpoint. As it stands, nothing is being done with the data being sent to the API endpoints. LMNH has asked our team to create a data model for processing this data, accounting for more recent and older data and also a visual represenation of the data, that is easy to understand by those from a noh-tehnical background.

## Project Objectives

To make effective use of the sensor data, we propose the following solutions:

- **Data Pipeline**: A cloud-hosted pipeline for data collection and processing, sending emails for anomalous recordings.
- **Short-term Storage Solution**: Stores data from the past 24 hours for real-time insights.
- **Long-term Storage Solution**: Retains data older than 24 hours for historical analysis.
- **Data Visualisation Dashboard**: A dashboard for stakeholders to visualise and understand plant health data.

With the described functionality, the LMNH will be able to monitor the health of plants and make informed decisions for the wellbeing of individual plants.
<br><br>

#### Figure 1: LMNH Botanical Garden Data Architecture
<img src="assets/lmnh_botany_data_architecture.png" alt="Data Visualisation" width="600"/>



## Repository Structure

Below is a high-level description of the key components within each directory of this repository.
<br>
**Exact details on how to run scripts from each directory can be found in dedicated directory READMEs.**

### 1. `pipeline/`

**Description**: This directory contains the data pipeline code responsible for processing sensor data. 
The scripts within this directory named below are run chronologically as listed.

- **Files**:
  - `extract.py`: Takes plant data from the provided LMNH plant API with multi-threading and returns a DataFrame.
  - `transform.py`: Takes in the DataFrame from extract.py, returning a formatted DataFrame controlled for types.
  - `load.py`: Connects to the LMNH botanical MS SQL Server database, and commits the transformed DataFrame to the 'recording' Table.
    #### Figure 2: ERD Diagram, illustrating the structure of our database storing plant data in 3NF. 
    <img src="assets/drawSQL-image-export-2024-10-04.png" alt="Data Visualisation" width="450"/>
    <br><br>
  - `emailing.py`: Automatically sends an alert email to the botanist if a plant's temperature or soil moisture levels found in the committed plant data are outside the acceptable range. Emails will outline an anomaly for a given plant recording, whether an upper or lower bound has been breached, what the plant ID is, and the botanist in charge of it.
    <br><br>

    #### Figure 3: Example anomaly emails for upper and lower plant temperature boundary conditions:

    <img src="assets/temp_high.png" alt="High Temperature Alert" width="360"/>
    <img src="assets/temp_low.png" alt="Low Temperature Alert" width="360"/>
    <br><br>
    
    #### Figure 4: Example anomaly emails for upper and lower plant soil moisture boundary conditions:

    <img src="assets/moisture_high.png" alt="High Moisture Alert" width="360"/>
    <img src="assets/moisture_low.png" alt="Low Moisture Alert" width="360"/>

    <br>
### 2. `seeding/`

**Description**: This directory contains the shell and .sql script(s) needed to connect to the RDS instance containing LMNH plant data remotely, and reset the database by dropped all tables in the event a wipe is necessary. The provided sql script can then be used to restore table structure and seed data.

- **Files**:
  - `connect.sh`: Connects to the remote RDS instance, where LMNH's plant data is being stored and constantly updated.
  - `schema.sql`: Defines the structure of all tables in the RDS, following the ERD and seeding the mapping tables 'plant', 'botanist' and 'location'. 
  - `reset.sh`: Uses the above 'schema.sql' script to first drop all tables, and then re-create all tables and re-insert seed data.


### 3. `terraform/`

**Description**: This directory contains the .tf files necessary for Terraform to automatically build the AWS cloud infrastructure that our data pipeline interacts with to store our data, send emails, and all other core aspects of this project's functionality.

- **Files**:
  - `main.tf`: Contains the instructions of exactly what and how to build the AWS resources needed for this project.
  - `variables.tf`: Contains the construction variables used to parameterise and configure AWS services being built.

### 4. `visualisation/`

**Description**:

- **Files**:
  - `dashboard.py`: Generates a Streamlit dashboard using Altair visualisations in Python. Allowing for temperature and soil moisture level recordings within the last 24 hours to be view in a clear manner, across all available plants. A measure of average value across all days is also available as a red line of best fit. Additional information regarding specific plants can also be found below, displaying scientific name, origin, and the information of the plant's linked botanist.

    #### Figure 5: Line graphs on the LMNH plant dashboard, showing variations in temperature and soil moisture across a day.
    <img src="assets/dashboard.png" alt="Data Visualisation" width="450"/>

    #### Figure 6: Visual presenting additional information about a select plant, with a picture to the left of easy identification.
    <img src="assets/plant_info.png" alt="Data Visualisation" width="450"/>
