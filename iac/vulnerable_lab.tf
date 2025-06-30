
---

## 2. `iac/vulnerable_lab.tf`  —— **故意“有洞”的实验环境**

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

/* 🚩 1. 公网暴露的 EC2 安全组 (0.0.0.0/0) */
resource "aws_security_group" "open_sg" {
  name        = "open-sg"
  description = "INTENTIONALLY open to the world"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]   # <-- 高危
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

/* 🚩 2. 公开读取权限的 S3 桶 */
resource "aws_s3_bucket" "public_bucket" {
  bucket = "demo-insecure-bucket-${random_id.rand.hex}"
  acl    = "public-read"        # <-- 高危
}

resource "random_id" "rand" {
  byte_length = 4
}
