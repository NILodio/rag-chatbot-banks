terraform {
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 4.0.0"
      }
      prefect = {
        source = "prefecthq/prefect"
      }
      docker = {
        source  = "kreuzwerker/docker"
        version = "~> 3.0.0"
      }
    }
}

provider "prefect" {
  account_id = var.prefect_account_id
  workspace_id = var.prefect_workspace_id
  api_key    = var.prefect_api_key
}

provider "aws" {
    region     = var.region
    access_key = var.aws_access_key_id
    secret_key = var.aws_secret_access_key
}

data "aws_region" "current" {}

resource "aws_secretsmanager_secret" "prefect_api_key" {
  name = "prefect-api-key-${var.name}-${var.stage}"
  force_overwrite_replica_secret = true
}

resource "aws_secretsmanager_secret_version" "prefect_api_key_version" {
  secret_id     = aws_secretsmanager_secret.prefect_api_key.id
  secret_string = var.prefect_api_key
}

resource "aws_ecr_repository" "ecr_repository" {
  name = "${var.name}-${var.stage}"
}

data "aws_ecr_authorization_token" "token" {}

provider "docker" {
  registry_auth {
    address  = data.aws_ecr_authorization_token.token.proxy_endpoint
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password
  }
}

resource "docker_image" "docker_image_prefect" {
  name = "${aws_ecr_repository.ecr_repository.repository_url}:latest"
  build {
    context    = "${path.module}/.."
    dockerfile = "Dockerfile"
  }
}

resource "docker_registry_image" "docker_registry_image_prefect" {
  name = docker_image.docker_image_prefect.name
  keep_remotely = true
}

resource "aws_iam_role" "prefect_worker_execution_role" {
  name = "prefect-worker-execution-role-${var.name}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })

  inline_policy {
    name = "ssm-allow-read-prefect-api-key-${var.name}"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "kms:Decrypt",
            "secretsmanager:GetSecretValue",
            "ssm:GetParameters"
          ]
          Effect = "Allow"
          Resource = [
            aws_secretsmanager_secret.prefect_api_key.arn
          ]
        }
      ]
    })
  }
  // AmazonECSTaskExecutionRolePolicy is an AWS managed role for creating ECS tasks and services
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"]
}

resource "aws_iam_role" "prefect_worker_task_role" {
  name  = "prefect-worker-task-role-${var.name}"
  count = var.worker_task_role_arn == null ? 1 : 0

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })

  inline_policy {
    name = "prefect-worker-allow-ecs-task-${var.name}"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "ec2:DescribeSubnets",
            "ec2:DescribeVpcs",
            "ecr:BatchCheckLayerAvailability",
            "ecr:BatchGetImage",
            "ecr:GetAuthorizationToken",
            "ecr:GetDownloadUrlForLayer",
            "ecs:DeregisterTaskDefinition",
            "ecs:DescribeTasks",
            "ecs:RegisterTaskDefinition",
            "ecs:RunTask",
            "ecs:TagResource",
            "iam:PassRole",
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:GetLogEvents",
            "logs:PutLogEvents"
          ]
          Effect   = "Allow"
          Resource = "*"
        }
      ]
    })
  }
}

resource "aws_cloudwatch_log_group" "prefect_worker_log_group" {
  name              = "prefect-worker-log-group-${var.name}"
  retention_in_days = var.worker_log_retention_in_days
}
