resource "tls_private_key" "registry" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "tls_self_signed_cert" "registry" {
  is_ca_certificate     = true
  allowed_uses          = ["cert-signing"]
  key_algorithm         = tls_private_key.registry.algorithm
  private_key_pem       = tls_private_key.registry.private_key_pem
  validity_period_hours = var.registry_ca_validity
  subject {
    common_name = local.deployment_name
  }
}

resource "google_pubsub_topic" "telemetry" {
  name = "${local.deployment_name}-telemetry"
}

resource "google_pubsub_topic" "devicestatus" {
  name = "${local.deployment_name}-devicestatus"
}

resource "google_cloudiot_registry" "registry" {
  name = local.deployment_name

  credentials {
    public_key_certificate = {
      format      = "X509_CERTIFICATE_PEM"
      certificate = tls_self_signed_cert.registry.cert_pem
    }
  }

  event_notification_configs {
    pubsub_topic_name = google_pubsub_topic.telemetry.id
    subfolder_matches = ""
  }

  state_notification_config = {
    pubsub_topic_name = google_pubsub_topic.devicestatus.id
  }

  http_config = {
    http_enabled_state = "HTTP_DISABLED"
  }

  log_level = "INFO"
}

