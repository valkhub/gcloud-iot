resource "local_file" "ca" {
  filename = "${path.module}/../auth/ca.pem"
  content = data.local_file.gcloud_root_cas.content
}

resource "local_file" "sensors_cert" {
  for_each = toset(local.sensors)
  filename = "${path.module}/../auth/sensors/${each.key}/cert.pem"
  content = module.sensors[each.key].cert_pem
}

resource "local_file" "sensors_key" {
  for_each = toset(local.sensors)
  filename = "${path.module}/../auth/sensors/${each.key}/key.pem"
  content = module.sensors[each.key].key_pem
}

resource "local_file" "actuators_cert" {
  for_each = toset(local.actuators)
  filename = "${path.module}/../auth/actuators/${each.key}/cert.pem"
  content = module.actuators[each.key].cert_pem
}

resource "local_file" "actuators_key" {
  for_each = toset(local.actuators)
  filename = "${path.module}/../auth/actuators/${each.key}/key.pem"
  content = module.actuators[each.key].key_pem
}
