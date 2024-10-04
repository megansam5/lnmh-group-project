# ETL Pipeline

## Overview

This folder should contain all code and resources required for the etl pipeline, which connects to the api, extracts all relevant plant data, cleans and processes the data for upload and them uploads the data to the RDS.

This has three main stages:
1. Extract: Retrieves records from each plant from the https://data-eng-plants-api.herokuapp.com/plants/ API endpoint.
2. Transform: Cleans the data, and if there is a recording outside the accepted range, emails the botanist.
3. Load: Loads the recordings into an RDS database.


## Folder Structure

- `extract.py`: Loops through the api plant pages extracting all the relevant data and then collates the data into a pandas DataFrame ready for cleaning and other activities. 
- `transform.py`: Analyses (sends alert emails), cleans and processes the passed DataFrame for upload.
- `load.py`: Uploads the recordings data to the rds. 
- `etl.py`: Connects and runs the previous files.
- `emailing.py`: Builds the email structure and content using html, querying the rds for relevant details and then sending the email to relevant botanists.
- `lambda_function.py`: Formats the pipeline for use with AWS lambda.
- `requirements.txt`: A text file containing all the dependencies needed for the folder to run.
- `Dockerfile`: Docker file to build an image of the pipeline.
- `test_extract.py`: Tests for the extract functionality.
- `test_transform.py`: Tests for the transforming functionality.
- `test_load.py`: Tests for the load functionality.
- `test_emailing.py`: Tests for the emailing functionality.
- `test_etl.py`: Tests for the whole pipeline.


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
DB_PORT=XXX
DB_PASSWORD=XXX
AWS_ACCESS_KEY=XXX
AWS_SECRET_KEY=XXX
BUCKET_NAME=XXX
SCHEMA_NAME=XXX
FROM_EMAIL=XXX
TO_EMAIL=XXX
```
5. Run the pipeline with `python3 etl.py`.


## As a Docker Container Locally

- Build the Image with `docker build -t pipeline-image .`
- Run a Container with `docker run --env-file .env pipeline-image .`


## Deploying to the Cloud

To deploy the pipeline:
- Authenticate docker with `aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com`
- Create an ECR repository with `aws ecr create-repository --repository-name c13-dog-botany-pipeline --region eu-west-2`
- Build the image with the correct platform with `docker build -t c13-dog-botany-pipeline . --platform "linux/amd64"`
- Tag the image with `docker tag c13-dog-botany-pipeline:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/c13-dog-botany-pipeline:latest`
- Push the image to the ECR with `docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/c13-dog-botany-pipeline:latest`
    
And then move into the [terraform directory](../terraform) to create the lambda.
    