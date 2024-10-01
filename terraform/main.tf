provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

# LAMBDA

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
      "rds:DescribeDBInstances",
      "rds:Connect",
      "Some other requirements"
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

# MINUTE SCHEDULE FOR LAMBDA

# Assuming the role for the schedule
data  "aws_iam_policy_document" "assume-min-schedule-role" {

    statement {
        effect = "Allow"

        principals {
            type        = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }

        actions = ["sts:AssumeRole"]
    }
}

# Permissions for the role: invoking a lambda, passing the IAM role
data  "aws_iam_policy_document" "min-schedule-permissions-policy" {

    statement {
        effect = "Allow"
        resources = [
                aws_lambda_function.pipeline_lambda.arn
            ]
        actions = [
            "lambda:Invoke"
        ]
    }

    statement {
        effect = "Allow"
        resources = [
            "*"
        ]
        actions = [
            "iam:PassRole"
        ]
    }
}

# IAM role for scheduler
resource "aws_iam_role" "iam_for_min_schedule" {
    name               = "c13-dog-minute-scheduler-role"
    assume_role_policy = data.aws_iam_policy_document.assume-min-schedule-role.json
}

# Adding policies to role
resource "aws_iam_role_policy" "min_schedule_role_policy" {
  name   = "c13-dog-minute-schedule-role-policy"
  role   = aws_iam_role.iam_for_min_schedule.id
  policy = data.aws_iam_policy_document.min-schedule-permissions-policy.json
}

# Minute schedule

resource "aws_scheduler_schedule" "minute-schedule" {
    name = "c13-dog-minute-schedule"
    flexible_time_window {
      mode = "OFF"
    }
    schedule_expression = "cron(* * * * ? *)"
    schedule_expression_timezone = "UTC+1"

    target {
        arn = aws_lambda_function.pipeline_lambda.arn 
        role_arn = aws_iam_role.iam_for_min_schedule.arn
    }
}

# TASK DEFINITION FOR MOVING DATA

# ECR with moving-data image
data "aws_ecr_image" "data_transfer_image" {
  repository_name = "c13-dog-data-transfer"
  image_tag       = "latest"
}

# IAM role for running ECS task (already a role)
data "aws_iam_role" "iam_for_task_def" {
  name = "ecsTaskExecutionRole"
}

# Task definition for ECS task
resource "aws_ecs_task_definition" "data-transfer-task-definition" {
  family = "c13-dog-data-transfer-task-def"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  execution_role_arn = data.aws_iam_role.iam_for_task_def.arn
  cpu       = 256
  memory    = 512
  container_definitions = jsonencode([
    {
      name      = "c13-dog-data-transfer"
      image     = data.aws_ecr_image.data_transfer_image.image_uri
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
      environment = [
        {
            name="EXAMPLE1"
            value="EXAMPLEVALUE1"
        },
        {
            name="EXAMPLE2"
            value="EXAMPLEVALUE2"
        }
      ]
      logConfiguration = {
                logDriver = "awslogs"
                "options": {
                    awslogs-group = "/ecs/c13-dog-data-transfer-task-def"
                    awslogs-stream-prefix = "ecs"
                    awslogs-region = "eu-west-2"
                    mode = "non-blocking"
                    max-buffer-size = "25m"
                }
      }
    }])
}


# DAILY SCHEDULER FOR TASK DEF

# Assuming the role for the schedule
data  "aws_iam_policy_document" "assume-daily-schedule-role" {

    statement {
        effect = "Allow"
        principals {
            type        = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }
        actions = ["sts:AssumeRole"]
    }
}

# Permissions for the role: running a task def, passing the IAM role, logging
data  "aws_iam_policy_document" "daily-schedule-permissions-policy" {

    statement {
        effect = "Allow"
        resources = [
                aws_ecs_task_definition.data-transfer-task-definition.arn
            ]
        actions = [
            "ecs:RunTask"
        ]
    }

    statement {
        effect = "Allow"
        resources = [
            "*"
        ]
        actions = [
            "iam:PassRole"
        ]
    }

       statement {
        effect = "Allow"
        resources = [
            "arn:aws:logs:*:*:*"
        ]
        actions = [
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "logs:CreateLogGroup"
        ]
    }
}

# IAM role for scheduler
resource "aws_iam_role" "iam_for_daily_schedule" {
    name               = "c13-dog-daily-scheduler-role"
    assume_role_policy = data.aws_iam_policy_document.assume-daily-schedule-role.json
}

# Adding policies to role
resource "aws_iam_role_policy" "daily_schedule_role_policy" {
  name   = "c13-dog-daily-schedule-role-policy"
  role   = aws_iam_role.iam_for_daily_schedule.id
  policy = data.aws_iam_policy_document.daily-schedule-permissions-policy.json
}

# The default security group
data "aws_security_group" "c13-default-sg" {
    id = var.SECURITY_GROUP_ID
}

# A public subnet
data "aws_subnet" "c13-public-subnet" {
  id = var.SUBNET_ID
}

# The cluster we will run tasks on
data "aws_ecs_cluster" "c13-cluster" {
    cluster_name = var.CLUSTER_NAME
}

# Schedule

resource "aws_scheduler_schedule" "daily-schedule" {
    name = "c13-dog-daily-schedule"
    flexible_time_window {
      mode = "OFF"
    }
    schedule_expression = "cron(0 9 * * ? *)"
    schedule_expression_timezone = "UTC+1"

    target {
        arn = data.aws_ecs_cluster.c13-cluster.arn 
        role_arn = aws_iam_role.iam_for_daily_schedule.arn
        ecs_parameters {
          task_definition_arn = aws_ecs_task_definition.data-transfer-task-definition.arn
          launch_type = "FARGATE"
          network_configuration { 
                subnets          = [data.aws_subnet.c13-public-subnet.id]
                security_groups  = [data.aws_security_group.c13-default-sg.id]
                assign_public_ip = true
            }
        }
    }
}

# DASHBOARD ECS TASK + SERVICE

# ECR with dashboard image
data "aws_ecr_image" "dashboard_image" {
  repository_name = "c13-dog-botany-dashboard"
  image_tag       = "latest"
}

# Task definition
resource "aws_ecs_task_definition" "dashboard_task_definition" {
  family = "c13-dog-dashboard-task-def"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  execution_role_arn = data.aws_iam_role.iam_for_task_def.arn
  cpu       = 512
  memory    = 1024
  container_definitions = jsonencode([
    {
      name      = "c13-dog-botany-dashboard"
      image     = data.aws_ecr_image.dashboard_image.image_uri
      essential = true
      portMappings = [
        {
          containerPort = 8501
          hostPort      = 8501
        }
      ]
      environment = [
        {
          name  = "EXAMPLE1"
          value = "EXAMPLEVALUE1"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/c13-dog-dashboard-task-def"
          awslogs-stream-prefix = "ecs"
          awslogs-region        = "eu-west-2"
          mode                  = "non-blocking"
          max-buffer-size       = "25m"
        }
      }
    }])
}

# ECS Service for dashboard
resource "aws_ecs_service" "dashboard_service" {
  name            = "c13-dog-botany-dashboard-service"
  cluster         = data.aws_ecs_cluster.c13-cluster.id
  task_definition = aws_ecs_task_definition.dashboard_task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = [data.aws_subnet.c13-public-subnet.id]
    security_groups  = [data.aws_security_group.c13-default-sg.id]
    assign_public_ip = true
  }
}



