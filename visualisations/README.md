# Botany Dashboard

## Overview

This folder contains  streamlit dashboard to visualise the plants temperature and soil moisture over the last 24 hours, along with it's average in the past. The dashboard also contains further information about each plant, including the origin location and botanist.

## Folder Structure
- `dashboard.py`: The main streamlit dashboard.
- `Dockerfile`: Allows the dashboard to be dockerised. 
- `requirements.txt`: The requirements for running this dashboard.

## Set-up and running locally

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
```
5. Build the dashboard with `docker build -t dashboard .`
6. Run the dashboard with `docker run -it -p 8501:8501 --env-file .env dashboard`

## Deploying

To deploy the dashboard

To deploy the pipeline:
- Authenticate docker with `aws ecr get-login-password --region YOUR_AWS_REGION | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com`
- Create an ECR repository with `aws ecr create-repository --repository-name c13-dog-botany-dashboard --region eu-west-2`
- Build the image with the correct platform with `docker build -t c13-dog-botany-dashboard . --platform "linux/amd64"`
- Tag the image with `docker tag c13-dog-botany-dashboard:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/c13-dog-botany-dashboard:latest`
- Push the image to the ECR with `docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/c13-dog-botany-dashboard:latest`

And then move into the `terraform` folder to create the task definition and service.