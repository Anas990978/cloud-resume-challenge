variable "aws_region" {
    description = "AWS region"
    type        = string
    default     = "us-east-1"
}

variable "table_name" {
    description = "DynamoDB table name"
    type        = string
    default     = "visitors"
}
variable "domain_name" {
    description = "Domain name for the website"
    type        = string
    default     = "anas-webiste.com"
}

