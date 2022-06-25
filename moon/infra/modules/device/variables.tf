variable "name" {}

variable "registry_ca_cert" {}

variable "registry_key_pem" {}

variable "registry_id" {}

variable "device_cert_validity" {
  default = 8760
}

variable "device_type" {
  default = "sensor"
}
