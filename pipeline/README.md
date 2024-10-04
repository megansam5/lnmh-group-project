# Pipeline

This folder should contain all code and resources required for the etl pipeline, which Connects to the api, extracts all relevant plant data 
cleans and processes the data for upload and them uploads the data to the rds. 


### Files

- `extract.py`
  - python script that loops through the api plant pages extracting all the relevant data and then collates the data into a pandas DataFrame ready for cleaning and other activities. 

- `transform.py`
  - This script analyses (sends alert emails), cleans and processes the passed DataFrame for upload.

- `load.py`
  - This script uploads the recordings data to the rds. 

- `etl.py`
  - python script that connects and runs the previous files.

- `emailing.py`
  - A python script that builds the email structure and content using html, querying the rds for relevant details and then sending the email to relevant botanists.

- `lambda_function.py`
  - Formats the pipeline for use with AWS lambda.

- `requirements.txt`
  - A text file containing all the dependencies needed for the folder to run.

- `Dockerfile`
  - Docker file to build an image of the pipeline.


### Development 

You will nee a .env file with the following structure.

```
AWS_ACCESS_KEY=xxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxx
DB_HOST=xxxxxxxxxxxxxxxx
DB_PORT=xxxxxxxxxxxxxxxx
DB_NAME=xxxxxxxxxxxxxxxx
DB_USER=xxxxxxxxxxxxxxxx
DB_PASSWORD=xxxxxxxxxxxxxxxx
SCHEMA_NAME=xxxxxxxxxxxxxxxx
FROM_EMAIL=xxxxxxxxxxxxxxxx
TO_EMAIL1=xxxxxxxxxxxxxxxx
TO_EMAIL2=xxxxxxxxxxxxxxxx
TO_EMAIL3=xxxxxxxxxxxxxxxx
TO_EMAIL4=xxxxxxxxxxxxxxxx
```

### Local 

You will need to create a venv and pip3 install the requirements.

    - Activate a `venv`
    - `pip3 install -r requirements.txt`
    - RUN 
    ```
    pip uninstall pymssql
    brew install freetds
    export CFLAGS="-I$(brew --prefix openssl)/include"
    export LDFLAGS="-L$(brew --prefix openssl)/lib -L/usr/local/opt/openssl/lib"
    export CPPFLAGS="-I$(brew --prefix openssl)/include"
    pip install --pre --no-binary :all: pymssql==2.2.11 --no-cache
    ```
    - `python3 etl.py`

### As a Docker Container Locally

    - Build the Image with `docker build -t pipeline-image .`
    - Run a Container with `docker run --env-file .env pipeline-image .`


### Cloud Deployment

    - Upload image to cloud
    ```
    aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com
    aws ecr create-repository --repository-name c13-dog-botany-pipeline --region eu-west-2
    docker build -t c13-dog-botany-pipeline . --platform "linux/amd64"
    docker tag c13-dog-botany-pipeline:latest 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c13-dog-botany-pipeline:latest
    docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c13-dog-botany-pipeline:latest
    ```
    - Run Terraform - Instructions in Terraform ReadMe
    

    