# Terraforming

This terraforming creates all the required AWS services, except the ECRs, for this project. This includes the lambda for the ETL pipeline, the eventbridge scheduler to run this every minute, the ECS Task definition to run the ECS Task to move the data from short term to long term, and its eventbridge scheduler every 24 hours, the task definition for the ECS service for the dashboard, along with all the necessary permissions and security groups.

## Set-up and Running

You need to create a `terraform.tfvars` file which includes the following:
```
AWS_ACCESS_KEY = "XXX"
AWS_SECRET_KEY = "XXX"
SECURITY_GROUP_ID = "XXX"
SUBNET_ID = "XXX"
CLUSTER_NAME = "XXX"
DB_HOST = "XXX"
DB_PASSWORD = "XXX"
DB_USER = "XXX"
DB_NAME = "XXX"
BUCKET_NAME = "XXX"
SCHEMA_NAME = "XXX"
VPC_ID = "XXX"
```

Before running this terraform script, you need to go into the `data-transfer-pipeline`, `pipeline`, and `visualisations` folders and follow the instructions to `Deploy`, which involves making the ECRs containing the Docker images.

To run first check with `terraform plan`.

Then run with `terraform apply`.

After use, destroy with `terraform destroy`. (The 3 ECRs will have to be manually deleted on the AWS UI.)