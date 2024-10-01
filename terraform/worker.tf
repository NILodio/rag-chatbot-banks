resource "prefect_work_pool" "worker_poll_name" {
  name         = "${var.worker_pool_name}-${var.stage}"
  type         = "ecs"
}
