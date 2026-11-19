terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # Remote state in S3 with native locking (Terraform >= 1.10).
  # Bucket, key and region are passed at init time:
  #   terraform init -backend-config=backend.hcl
  # See terraform/README.md.
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = var.project
      ManagedBy = "terraform"
      Owner     = "hulaneoTi"
    }
  }
}
