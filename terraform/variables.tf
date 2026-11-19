variable "project" {
  description = "Name prefix for every resource."
  type        = string
  default     = "devsecops-30-days"
}

variable "aws_region" {
  description = "AWS region for the sandbox."
  type        = string
  default     = "us-east-1"
}

variable "allowed_cidr" {
  description = "Only this CIDR can reach the app (use your public IP with /32)."
  type        = string

  validation {
    condition     = can(cidrhost(var.allowed_cidr, 0)) && var.allowed_cidr != "0.0.0.0/0"
    error_message = "allowed_cidr must be a valid CIDR and cannot be 0.0.0.0/0."
  }
}

variable "instance_type" {
  description = "EC2 instance type (free tier eligible)."
  type        = string
  default     = "t3.micro"
}

variable "app_image" {
  description = "Container image published by the CI pipeline."
  type        = string
  default     = "ghcr.io/hulaneoti/devsecops-30-days:latest"
}
