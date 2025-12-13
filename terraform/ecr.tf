resource "aws_ecr_repository" "services" {
  for_each = toset([
    "frontend",
    "api-gateway",
    "ms-usuarios",
    "ms-espacos",
    "ms-reservas",
    "ms-pagamentos",
    "ms-precos",
    "ms-checkin",
    "ms-notificacoes",
    "ms-financeiro",
    "ms-analytics"
  ])

  name                 = "${var.project_name}/${each.key}"
  image_tag_mutability = "MUTABLE"
  force_delete         = true # CUIDADO: Permite destruir repositório com imagens

  image_scanning_configuration {
    scan_on_push = true
  }
}
