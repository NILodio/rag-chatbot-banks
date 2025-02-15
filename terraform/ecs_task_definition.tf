resource "aws_ecs_task_definition" "prefect_worker_task_definition" {
  family = "prefect-worker-${var.name}-${var.stage}"
  cpu    = var.worker_cpu
  memory = var.worker_memory

  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"

  container_definitions = jsonencode([
    {
      name    = "prefect-worker-${var.name}"
      image   = docker_image.docker_image_prefect.name
      command = ["prefect", "worker", "start", "--pool", "${prefect_work_pool.worker_poll_name.name}","--type","ecs"]
      cpu     = var.worker_cpu
      memory  = var.worker_memory
      environment = [
        {
          name  = "PREFECT_API_URL"
          value = "https://api.prefect.cloud/api/accounts/${var.prefect_account_id}/workspaces/${var.prefect_workspace_id}"
        },
      ]
      secrets = [
        {
          name      = "PREFECT_API_KEY"
          valueFrom = aws_secretsmanager_secret.prefect_api_key.arn
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.prefect_worker_log_group.name
          awslogs-region        = data.aws_region.current.name
          awslogs-stream-prefix = "prefect-worker-${var.name}-${var.stage}"
        }
      }
    }
  ])
  execution_role_arn = aws_iam_role.prefect_worker_execution_role.arn
  task_role_arn = var.worker_task_role_arn == null ? aws_iam_role.prefect_worker_task_role[0].arn : var.worker_task_role_arn
}

resource "aws_ecs_service" "prefect_worker_service" {
  name          = "prefect-worker-${var.name}-${var.stage}"
  cluster       = aws_ecs_cluster.prefect_worker_cluster.id
  desired_count = var.worker_desired_count
  launch_type   = "FARGATE"

  // Public IP required for pulling secrets and images
  // https://aws.amazon.com/premiumsupport/knowledge-center/ecs-unable-to-pull-secrets/
  network_configuration {
    security_groups  = [aws_security_group.prefect_worker.id]
    assign_public_ip = true
    subnets          = var.worker_subnets
  }
  task_definition = aws_ecs_task_definition.prefect_worker_task_definition.arn
}
