resource "random_string" "deployment_id" {
  length = 6
  special = false
}

locals {
  deployment_name = "clothworks_hdm_${random_string.deployment_id.result}"
  gcp_iot_mqtt = "mqtt.googleapis.com:8883"
}

locals {
  sensors = ["cloth", "silk", "wool"]
  actuators = ["cloth", "silk", "wool"]
}

data "local_file" "gcloud_root_cas" {
  filename = "creds/roots.pem"
}
