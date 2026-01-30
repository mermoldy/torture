variable "small_resource_count" {
  description = "Number of small resources to create. Small resources are low-cost to plan."
  type        = number
  default     = 1000
}

variable "medium_resource_count" {
  description = "Number of medium resources to create. Medium resources are medium-cost to plan."
  type        = number
  default     = 1000
}

variable "heavy_resource_count" {
  description = "Number of heavy resources to create. Heavy resources are expensive to plan."
  type        = number
  default     = 1000
}

variable "medium_log_lines_per_resource" {
  description = "Number of log lines generated while applying each medium resource"
  type        = number
  default     = 10
}

variable "heavy_log_lines_per_resource" {
  description = "Number of log lines generated while applying each heavy resource"
  type        = number
  default     = 1000
}

variable "enable_providers" {
  description = "Enable installation of 50 providers during terraform init"
  type        = bool
  default     = false
}

variable "enable_modules" {
  description = "Enable loading of 50 git modules during terraform init"
  type        = bool
  default     = false
}

variable "local_files_count" {
  description = "Number of local files to create during initialization (0 to disabled)"
  type        = number
  default     = 0

  validation {
    condition     = var.local_files_count >= 0 && var.local_files_count <= 100000
    error_message = "Local files count must be between 0 and 100000."
  }
}
