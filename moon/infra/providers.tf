provider "google" {
  project     = var.gcp_project_id
  region      = var.gcp_region
  credentials = file("creds/clothworks-hdm-key.json")
}
