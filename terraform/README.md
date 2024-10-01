# Terraforming

This terraforming creates the lambda for the ETL pipeline, the eventbridge scheduler to run this every minute, the ECS Task definition to run the ECS Task to move the data from short term to long term, and its eventbridge scheduler every 24 hours. And also the task definition for the ECS service for the dashboard.