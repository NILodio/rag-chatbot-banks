variable "aws_access_key_id" {
  description = "AWS access key ID"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS secret access key"
  type        = string
  
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "worker_cpu" {
  description = "CPU units to allocate to the worker"
  default     = 1024
  type        = number
}

variable "worker_desired_count" {
  description = "Number of workers to run"
  default     = 1
  type        = number
}

variable "worker_extra_pip_packages" {
  description = "Packages to install on the worker assuming image is based on prefecthq/prefect"
  default     = "prefect-aws s3fs"
  type        = string
}

variable "worker_image" {
  description = "Container image for the worker. This could be the name of an image in a public repo or an ECR ARN"
  default     = "prefecthq/prefect:3-python3.9"
  type        = string
}

variable "worker_log_retention_in_days" {
  description = "Number of days to retain worker logs for"
  default     = 30
  type        = number
}

variable "worker_memory" {
  description = "Memory units to allocate to the worker"
  default     = 2048
  type        = number
}

variable "worker_poll_name" {
  description = "Prefect cloud poll name"
  default     = "rag-chatbot-banks-poll"
  type        = string
}

variable "worker_subnets" {
  description = "Subnets to place the worker in"
  type        = list(string)
}

variable "worker_task_role_arn" {
  description = "Optional task role ARN to pass to the worker. If not defined, a task role will be created"
  default     = null
  type        = string
}

variable "name" {
  description = "Unique name for this worker deployment"
  default     = "rag-chatbot-banks-worker-test-2"
  type        = string
}

variable "prefect_account_id" {
  description = "Prefect cloud account ID"
  type        = string
}

variable "prefect_workspace_id" {
  description = "Prefect cloud workspace ID"
  type        = string
}

variable "prefect_api_key" {
  description = "Prefect cloud API key"
  type        = string
  sensitive   = true
}

variable "vpc_id" {
  description = "VPC ID in which to create all resources"
  type        = string
}

variable "bucket_name" {
  description = "S3 bucket"
  default     = "rag-chatbot-banks"
  type        = string
}
