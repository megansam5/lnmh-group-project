# Daily Data Transfer Pipeline

## Overview

This folder contains a Python-based ETL (Extract, Transform, Load) pipeline for transferring old plant recording data from the RDS database to the S3 bucket in Parquet format. The pipeline runs daily, extracting data that is older than 24 hours, saving it to S3, and then deleting the old data from the RDS database and updating the averages table.

This has three main stages:
1. Extract: Retrieve data older than 24 hours from the RDS database.
2. Load: Save the extracted data into S3 in Parquet format, organized by date.
3. Clean: Delete the old data from the RDS once it has been successfully transferred, and updates the current averages for each plant based on new recordings.

## Folder Structure

- `extract.py`: Handles the extraction of data from RDS.
- `load.py`: Handles loading the extracted data to S3.
- `clean.py`: Cleans old data from the RDS and updates the plant_average table.
- `pipeline.py`: Main script to run the full ETL pipeline.
- `Dockerfile`: Docker file to build an image of the pipeline.             
- `requirements.txt`: The requirements for running this pipeline.
- `connect.sh`: A quick shell script to connect to the database.
- `test_extract.py`: Tests for the extract functionality.
- `test_load.py`: Tests for the load functionality.
- `test_clean.py`: Tests for the clean functionality.
- `test_pipeline.py`: Tests for the whole pipeline.

## Set-up and Running Locally

1. Create a virtual environment.
2. Install dependencies by running `pip install -r requirements.txt`
3. Run the following commands to get the correct pymssql:
```
pip uninstall pymssql
brew install freetds
export CFLAGS="-I$(brew --prefix openssl)/include"
export LDFLAGS="-L$(brew --prefix openssl)/lib -L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I$(brew --prefix openssl)/include"
pip install --pre --no-binary :all: pymssql==2.2.11 --no-cache
```
4. Create a `.env` file with the following:
```
DB_HOST=XXX
DB_NAME=XXX
DB_USER=XXX
DB_PASSWORD=XXX
AWS_ACCESS_KEY=XXX
AWS_SECRET_KEY=XXX
BUCKET_NAME=XXX
SCHEMA_NAME=XXX
```
5. Run the pipeline with `python3 pipeline.py`.

## As a Docker Container Locally

- Build the Image with `docker build -t pipeline-image .`
- Run a Container with `docker run --env-file .env pipeline-image .`

## Deploying to the Cloud

To deploy the pipeline:
- Authenticate docker with `aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com`
- Create an ECR repository with `aws ecr create-repository --repository-name c13-dog-data-transfer --region eu-west-2`
- Build the image with the correct platform with `docker build -t c13-dog-data-transfer . --platform "linux/amd64"`
- Tag the image with `docker tag c13-dog-data-transfer:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/c13-dog-data-transfer:latest`
- Push the image to the ECR with `docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/c13-dog-data-transfer:latest`

And then move into the [terraform directory](../terraform) to create the task definition.

