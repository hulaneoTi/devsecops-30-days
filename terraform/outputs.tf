output "app_url" {
  description = "URL of the app (reachable only from allowed_cidr)."
  value       = "http://${aws_instance.app.public_ip}:8080/health"
}

output "instance_id" {
  description = "Use with: aws ssm start-session --target <id>"
  value       = aws_instance.app.id
}
