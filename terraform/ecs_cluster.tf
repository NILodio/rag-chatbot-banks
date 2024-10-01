
resource "aws_ecs_cluster" "prefect_worker_cluster" {
  name = "prefect-worker-${var.name}-${var.stage}"
}

resource "aws_ecs_cluster_capacity_providers" "prefect_worker_cluster_capacity_providers" {
  cluster_name       = aws_ecs_cluster.prefect_worker_cluster.name
  capacity_providers = ["FARGATE"]
}
