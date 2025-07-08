output "dynamodb_table_name" {
    value = aws_dynamodb_table.visitors.name
}
output "api_url" {
    value = "${aws_api_gateway_deployment.api_deployment.invoke_url}/visitors"
}
output "website_url" {
    value = "https://${aws_cloudfront_distribution.website.domain_name}"
}

output "s3_bucket_name" {
    value = aws_s3_bucket.website.bucket
}

output "custom_domain_url" {
    value = "https://${var.domain_name}"
}
