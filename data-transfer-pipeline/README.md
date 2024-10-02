# Daily Data Transfer Pipeline

## Things still to do:

- Check which columns want to be stored in s3. (at the moment only columns from recording as can link back to RDS)
- Check the connection works in Dockerfile (check with coaches)
- Check this works with around 72,000 rows of data (should take ~30/40 seconds) - optimize if not


## Overview

This folder contains a Python-based ETL (Extract, Transform, Load) pipeline for transferring old plant recording data from the RDS database to the S3 bucket in Parquet format. The pipeline runs daily, extracting data that is older than 24 hours, saving it to S3, and then deleting the old data from the RDS database.

This has three main stages:
1. Extract: Retrieve data older than 24 hours from the RDS database.
2. Load: Save the extracted data into S3 in Parquet format, organized by date.
3. Clean: Delete the old data from the RDS once it has been successfully transferred.

## Folder Structure

- `extract.py`: Handles the extraction of data from RDS.
- `load.py`: Handles loading the extracted data to S3.
- `clean.py`: Cleans old data from the RDS.
- `pipeline.py`: Main script to run the full ETL pipeline.
- `Dockerfile`: Allows the pipeline to be dockerized.              
- `test_extract.py`: Tests for the extract functionality.
- `test_load.py`: Tests for the load functionality.
- `test_clean.py`: Tests for the clean functionality.
- `test_pipeline.py`: Tests for the whole pipeline.

## Set-up

1. Create a virtual environment.
2. Install dependencies by running `pip install -r requirements.txt`
3. Create a `.env` file with the following:
```
DB_HOST=<your-database-host>
DB_NAME=<your-database-name>
DB_USER=<your-database-username>
DB_PASSWORD=<your-database-password>
AWS_ACCESS_KEY=<your-aws-access-key>
AWS_SECRET_KEY=<your-aws-secret-key>
BUCKET_NAME=<your-s3-bucket-name>
SCHEMA_NAME=<your-database-schema>
```

## Running the pipeline

Run the pipeline with `python3 pipeline.py`.

