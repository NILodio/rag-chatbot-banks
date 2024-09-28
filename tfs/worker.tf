resource "prefect_work_pool" "worker_poll_name" {
  name         = var.worker_poll_name
  type         = "ecs"
}
