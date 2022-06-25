module "sensors" {
  for_each         = toset(local.sensors)
  source           = "./modules/device"
  name             = "sensor-${each.key}"
  registry_ca_cert = tls_self_signed_cert.registry
  registry_id      = google_cloudiot_registry.registry.id
  registry_key_pem = tls_private_key.registry.private_key_pem
}

module "actuators" {
  for_each         = toset(local.actuators)
  source           = "./modules/device"
  device_type      = "actuator"
  name             = "actuator-${each.key}"
  registry_ca_cert = tls_self_signed_cert.registry
  registry_id      = google_cloudiot_registry.registry.id
  registry_key_pem = tls_private_key.registry.private_key_pem
}
