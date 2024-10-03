provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

# S3 bucket for Athena output - use your existing bucket for results
locals {
  s3_data_bucket   = "c13-dog-botany-long-term"   # Existing bucket
  athena_results   = "s3://c13-dog-botany-long-term/results/" # Results folder
}

# IAM Role with assume role for glue and athena
resource "aws_iam_role" "glue_athena_role" {
  name = "c13-dog-glue_athena_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "glue.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      },
      {
        Effect = "Allow",
        Principal = {
          Service = "athena.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# added policies for glue and athena ------ 
resource "aws_iam_policy" "glue_athena_s3_policy" {
  name        = "c13-dog-glue_athena_s3_policy"
  policy      = jsonencode({
    Version: "2012-10-17",
    Statement: [
      {
        Effect: "Allow",
        Action: [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource: [
          "arn:aws:s3:::${local.s3_data_bucket}",
          "arn:aws:s3:::${local.s3_data_bucket}/*"
        ]
      },
      {
        Effect: "Allow",
        Action: [
          "glue:GetDatabase",
          "glue:GetTable",
          "glue:CreateTable",
          "glue:GetPartitions",
          "glue:BatchCreatePartition"
        ],
        Resource: "*"
      },
      {
        Effect: "Allow",
        Action: [
          "athena:StartQueryExecution",
          "athena:GetQueryExecution",
          "athena:GetQueryResults",
          "athena:GetWorkGroup"
        ],
        Resource: "*"
      },
      {
        Effect: "Allow",
        Action: [
          "athena:ListWorkGroups"
        ],
        Resource: "*"
      }
    ]
  })
}

# Attach IAM policy to the role
resource "aws_iam_role_policy_attachment" "glue_athena_policy_attachment" {
  role       = aws_iam_role.glue_athena_role.name
  policy_arn = aws_iam_policy.glue_athena_s3_policy.arn
}

# Glue Crawler (creates schema of s3)
resource "aws_glue_crawler" "plant_recordings_crawler" {
  name         = "c13-dog-plant-recordings-crawler"
  role         = aws_iam_role.glue_athena_role.arn
  database_name = aws_glue_catalog_database.botany_db.name 

  s3_target {
    path = "s3://${local.s3_data_bucket}/plant_recordings/"
  }

  schedule = "cron(0 8 * * ? *)"  

  configuration = jsonencode({
    "Version"                  : 1.0,
    "Grouping"                 : { "TableGroupingPolicy" : "CombineCompatibleSchemas" },
    "CrawlerOutput"            : { "Partitions" : { "AddOrUpdateBehavior" : "InheritFromTable" } }
  })

  depends_on = [aws_iam_role.glue_athena_role]
}

# Athena Workgroup
resource "aws_athena_workgroup" "plant_workgroup" {
  name = "c13-dog-plant-workgroup"
  configuration {
    enforce_workgroup_configuration = true
    publish_cloudwatch_metrics_enabled = true
    result_configuration {
      output_location = local.athena_results
    }
  }
}

# Glue Database 
resource "aws_glue_catalog_database" "botany_db" {
  name = "c13_dog_botany_db"
}

# Glue Catalog Table 
resource "aws_glue_catalog_table" "plant_recordings_table" {
  name          = "plant_recordings"
  database_name = aws_glue_catalog_database.botany_db.name

  table_type = "EXTERNAL_TABLE"

  storage_descriptor {
    location = "s3://${local.s3_data_bucket}/plant_recordings/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    columns {
      name = "recording_id"
      type = "bigint"
    }
    columns {
      name = "plant_id"
      type = "bigint"
    }
    columns {
      name = "recording_taken"
      type = "timestamp"
    }
    columns {
      name = "last_watered"
      type = "timestamp"
    }
    columns {
      name = "soil_moisture"
      type = "double"
    }
    columns {
      name = "temperature"
      type = "double"
    }

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }
  }

  partition_keys {
    name = "year"
    type = "int"
  }
  partition_keys {
    name = "month"
    type = "int"
  }
  partition_keys {
    name = "day"
    type = "int"
  }
}

# Athena table creation 
resource "null_resource" "create_athena_table" {
  provisioner "local-exec" {
    command = <<-EOT
      aws athena start-query-execution \
        --query-string "CREATE EXTERNAL TABLE IF NOT EXISTS c13_dog_botany_db.plant_recordings (
            recording_id BIGINT,
            plant_id BIGINT,
            recording_taken TIMESTAMP,
            last_watered TIMESTAMP,
            soil_moisture DOUBLE,
            temperature DOUBLE
          ) 
          PARTITIONED BY (year INT, month INT, day INT) 
          STORED AS PARQUET 
          LOCATION 's3://${local.s3_data_bucket}/plant_recordings/'" \
        --result-configuration "OutputLocation=${local.athena_results}" \
        --work-group ${aws_athena_workgroup.plant_workgroup.name}
    EOT
  }
  
  depends_on = [
    aws_glue_catalog_table.plant_recordings_table,
    aws_athena_workgroup.plant_workgroup
  ]
}
