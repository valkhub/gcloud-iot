resource "local_file" "compose_override" {
  filename = "${path.module}/../docker-compose.override.yml"
  content = templatefile("templates/docker-compose.override.yml.tftpl", {
    project_id = var.gcp_project_id
    sensors = module.sensors
    actuators = module.actuators
    broker = local.gcp_iot_mqtt
  })
}
