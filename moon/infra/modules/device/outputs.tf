output "device" {
  value = google_cloudiot_device.device
}

output "cert_pem" {
  value = tls_locally_signed_cert.device_cert.cert_pem
}

output "key_pem" {
  value = tls_private_key.device_keypair.private_key_pem
}
