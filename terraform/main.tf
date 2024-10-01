provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

# ECR with pipeline image
data "aws_ecr_image" "pipeline_image" {
  repository_name = "c13-dog-botany-pipeline"
  image_tag       = "latest"
}

# Assuming the role for the lambda
data "aws_iam_policy_document" "assume_lambda_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

#Permissions for role: inserting to database
data "aws_iam_policy_document" "lambda_permissions_policy" {
  statement {
    effect = "Allow"

    actions = [
      "???? - something to do with acessing RDS"
    ]

    resources = ["*"] 
  }
}

# IAM role for lambda
resource "aws_iam_role" "iam_for_lambda" {
  name               = "c13-dog-lambda-exec-role"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role.json
}

# Adding policies to role
resource "aws_iam_role_policy" "lambda_role_policy" {
  name   = "c13-dog-lambda-role-policy"
  role   = aws_iam_role.iam_for_lambda.id
  policy = data.aws_iam_policy_document.lambda_permissions_policy.json
}

# The lambda function
resource "aws_lambda_function" "pipeline_lambda" {
  function_name = "c13-dog-pipeline-lambda"
  role          = aws_iam_role.iam_for_lambda.arn

  package_type = "Image"
  timeout = 30
  memory_size = 512

  image_uri = data.aws_ecr_image.pipeline_image.image_uri

  environment {
    variables = {
      # Needed values for lambda 
    }
  }
}