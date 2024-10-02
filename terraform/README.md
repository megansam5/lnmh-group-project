# Terraforming

This terraforming creates the lambda for the ETL pipeline, the eventbridge scheduler to run this every minute, the ECS Task definition to run the ECS Task to move the data from short term to long term, and its eventbridge scheduler every 24 hours. And also the task definition for the ECS service for the dashboard.

## Set-up

YOu need to create a `terraform.tfvars` file which includes the following:
```
AWS_ACCESS_KEY = "XXX"
AWS_SECRET_KEY = "XX"
SECURITY_GROUP_ID = "XXX"
SUBNET_ID = "XXX"
CLUSTER_NAME = "XXX"
```
Along with any environmental variables needed for the lambda and task definitions.