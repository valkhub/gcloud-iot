resource "tls_private_key" "device_keypair" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_cert_request" "device_cert_req" {
  key_algorithm   = tls_private_key.device_keypair.algorithm
  private_key_pem = tls_private_key.device_keypair.private_key_pem
  subject {
    common_name = var.name
  }
}

resource "tls_locally_signed_cert" "device_cert" {
  allowed_uses          = ["client_auth"]
  ca_cert_pem           = var.registry_ca_cert.cert_pem
  ca_key_algorithm      = var.registry_ca_cert.key_algorithm
  ca_private_key_pem    = var.registry_key_pem
  cert_request_pem      = tls_cert_request.device_cert_req.cert_request_pem
  validity_period_hours = var.device_cert_validity
}

resource "google_cloudiot_device" "device" {
  name     = var.name
  registry = var.registry_id

  credentials {
    public_key {
      format = "RSA_X509_PEM"
      key    = tls_locally_signed_cert.device_cert.cert_pem
    }
  }

  metadata = {
    type = var.device_type
  }

  log_level = "INFO"
}
