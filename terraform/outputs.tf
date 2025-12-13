output "alb_dns_name" {
  description = "DNS do Load Balancer (Acesso Público)"
  value       = aws_lb.main.dns_name
}

output "rds_endpoint" {
  description = "Endpoint do Banco de Dados RDS"
  value       = aws_db_instance.postgres.address
}

output "ecr_repository_urls" {
  description = "URLs dos repositórios ECR criados"
  value       = [for repo in aws_ecr_repository.services : repo.repository_url]
}
