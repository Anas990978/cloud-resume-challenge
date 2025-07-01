output "dynamodb_table_name" {
    value = aws_dynamodb_table.visitors.name
}
output "api_url" {
    value = "${aws_api_gateway_deployment.api_deployment.invoke_url}/visitors"
}
