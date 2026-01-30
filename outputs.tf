output "initialization_summary" {
  description = "Summary of initialization resources"
  value = {
    providers_enabled = var.enable_providers
    modules_enabled   = var.enable_modules
    local_files_count = var.local_files_count
  }
}

output "resource_summary" {
  description = "Summary of all resources created"
  value = {
    small_resources  = var.small_resource_count
    medium_resources = var.medium_resource_count
    heavy_resources  = var.heavy_resource_count
    total_resources  = var.small_resource_count + var.medium_resource_count + var.heavy_resource_count
  }
}
