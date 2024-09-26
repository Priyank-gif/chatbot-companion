variable "app_name" {
  description = "The name of the application"
  type        = string
}

variable "environment" {
  description = "The environment for the application (e.g., production, development)"
  type        = string
}

variable "common_tags" {
  description = "Common tags to be applied to all resources"
  type        = map(string)
  default     = {
    Project     = "chatbot-companion"
    Environment = "development"  # Change as needed
  }
}
