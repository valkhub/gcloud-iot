#output "sensors" {
#  value = {
#  for k, v in module.sensors : k => {
#    id : v.device.id
#    auth : "auth/sensors/${k}"
#    broker : local.gcp_iot_mqtt
#  }
#  }
#  sensitive = false
#}

#output "actuators" {
#  value = {
#  for k, v in module.actuators : k => {
#    id : v.device.id
#    auth : "auth/actuators/${k}"
#    broker : local.gcp_iot_mqtt
#  }
#  }
#  sensitive = false
#}
