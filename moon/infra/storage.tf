resource "google_storage_bucket" "function_bucket" {
    name     = "${var.gcp_project_id}-function"
    location = var.gcp_region
}

resource "google_storage_bucket" "input_bucket" {
    name     = "${var.gcp_project_id}-input"
    location = var.gcp_region
}
