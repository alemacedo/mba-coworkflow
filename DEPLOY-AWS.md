# Guia de Deploy AWS - CoworkFlow

Este documento detalha o roteiro para preparar a infraestrutura na AWS (Amazon Web Services) para hospedar a aplicação CoworkFlow utilizando uma arquitetura de microsserviços containerizados.

## 1. Visão Geral da Infraestrutura

A aplicação será hospedada utilizando os seguintes serviços gerenciados:

*   **AWS ECR (Elastic Container Registry):** Armazenamento das imagens Docker dos microsserviços.
*   **AWS ECS (Elastic Container Service) + Fargate:** Orquestração e execução dos containers sem necessidade de gerenciar servidores (Serverless).
*   **AWS RDS (Relational Database Service):** Banco de dados PostgreSQL gerenciado.
*   **AWS ALB (Application Load Balancer):** Distribuição de tráfego e roteamento para o API Gateway e Frontend.

## 2. Passo 1: Repositórios ECR

Você deve criar um repositório ECR privado para **cada** serviço listado abaixo. Isso pode ser feito via Console AWS ou CLI (`aws ecr create-repository --repository-name <NOME>`).

**Nomes dos Repositórios:**
1.  `coworkflow/frontend`
2.  `coworkflow/api-gateway`
3.  `coworkflow/ms-usuarios`
4.  `coworkflow/ms-espacos`
5.  `coworkflow/ms-reservas`
6.  `coworkflow/ms-pagamentos`
7.  `coworkflow/ms-precos`
8.  `coworkflow/ms-checkin`
9.  `coworkflow/ms-notificacoes`
10. `coworkflow/ms-financeiro`
11. `coworkflow/ms-analytics`

## 3. Passo 2: Banco de Dados (RDS)

Crie uma instância de banco de dados para a aplicação.

*   **Engine:** PostgreSQL (versão 13 ou superior recomendada).
*   **Template:** Free tier ou Production (conforme necessidade).
*   **Identificador:** `coworkflow-db`.
*   **Credenciais:**
    *   **Master username:** `postgres` (ou outro de sua escolha).
    *   **Master password:** Gere uma senha forte (será usada nas variáveis de ambiente).
*   **Public Access:** `No` (por segurança, o acesso deve ser apenas de dentro da VPC).
*   **Security Group:** Deve permitir entrada na porta `5432` vindo do Security Group do ECS.

> **Nota:** Após criar o RDS, anote o `Endpoint` (host) gerado.

## 4. Passo 3: Cluster ECS e Networking

1.  **Criar Cluster ECS:**
    *   Nome: `coworkflow-cluster`.
    *   Template: `Networking only` (Powered by AWS Fargate).

2.  **Application Load Balancer (ALB):**
    *   Crie um ALB internet-facing.
    *   Defina **Target Groups** (tipo IP) para os serviços que precisam de acesso externo (principalmente Frontend e API Gateway).
    *   Configure Listeners (HTTP/80 e HTTPS/443 se tiver certificado).

## 5. Passo 4: Task Definitions (Definição das Tarefas)

Para cada microsserviço, crie uma **Task Definition** no ECS (Fargate).

**Configuração Padrão Sugerida por Task:**
*   **CPU:** `.25 vCPU`
*   **Memory:** `0.5 GB`
*   **Container Image URI:** `<ID_DA_CONTA>.dkr.ecr.<REGIAO>.amazonaws.com/coworkflow/<NOME_DO_SERVICO>:latest`
*   **Port Mappings:** A porta interna que o container usa (ex: 5000, 3000, etc - verifique no `docker-compose.yml` ou Dockerfiles).

**Variáveis de Ambiente (Environment Variables):**
Todos os serviços que acessam o banco devem ter as seguintes variáveis configuradas na Task Definition:

| Variável | Valor (Exemplo) |
| :--- | :--- |
| `DB_HOST` | `coworkflow-db...rds.amazonaws.com` (Endpoint do RDS) |
| `DB_NAME` | `coworkflow` |
| `DB_USER` | `postgres` |
| `DB_PASSWORD` | `<SUA_SENHA_DO_RDS>` |
| `FLASK_ENV` | `production` |

*O `ms-notificacoes` precisará de variáveis adicionais de SMTP se configurado.*

## 6. Passo 5: Services (Execução)

No cluster `coworkflow-cluster`, crie um **Service** para cada Task Definition criada.

*   **Launch Type:** Fargate.
*   **Desired Tasks:** 1 (ou mais para alta disponibilidade).
*   **Networking:** Selecione a mesma VPC e Subnets do ALB.
*   **Security Group:** Permitir entrada na porta do serviço vindo do ALB ou dos outros containers (para comunicação interna).

## 7. Passo 6: Configuração do Pipeline (GitHub Actions)

Para que o GitHub consiga conectar na sua conta AWS e atualizar os serviços, seguiremos este protocolo seguro.

### 6.1. Criar Usuário IAM para o CI/CD

1.  No Console AWS, vá em **IAM** -> **Users** -> **Create user**.
2.  Nome: `github-actions-deployer`.
3.  Não habilite acesso ao console.
4.  Em "Permissions", escolha **Attach policies directly**.
5.  Crie uma política customizada (JSON) com as permissões mínimas necessárias:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:PutImage"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ecs:UpdateService",
                "ecs:DescribeServices"
            ],
            "Resource": [
                "arn:aws:ecs:*:*:service/coworkflow-cluster/*"
            ]
        }
    ]
}
```

6.  Após criar, vá na aba **Security credentials** do usuário e crie uma **Access Key**.
7.  Copie a `Access Key ID` e a `Secret Access Key`.

### 6.2. Configurar Segredos no GitHub

No seu repositório GitHub, vá em **Settings** > **Secrets and variables** > **Actions** e crie os seguintes Repository secrets:

*   `AWS_ACCESS_KEY_ID`: (Valor copiado do passo anterior)
*   `AWS_SECRET_ACCESS_KEY`: (Valor copiado do passo anterior)
*   `AWS_REGION`: `us-east-1` (ou a região que você escolheu)

### 6.3. Atualizar o Workflow (ci-cd.yml)

Substitua a etapa de deploy do seu arquivo `.github/workflows/ci-cd.yml` pelo modelo abaixo. Este exemplo mostra como fazer o build e deploy de UM serviço. Você deve replicar os passos para os outros serviços.

```yaml
jobs:
  # ... (jobs de lint e test permanecem iguais)

  deploy:
    name: Build & Deploy to AWS
    runs-on: ubuntu-latest
    needs: test # Só faz deploy se passar nos testes
    if: github.ref == 'refs/heads/main' # Só deploy na branch main
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ secrets.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    # --- BLOCO REPLICÁVEL PARA CADA SERVIÇO ---
    - name: Build and Push MS-Usuarios
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: coworkflow/ms-usuarios
        IMAGE_TAG: ${{ github.sha }}
      run: |
        # Build
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG ./ms-usuarios
        # Push tag específica
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        # Tag latest para facilitar
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

    - name: Update ECS Service MS-Usuarios
      run: |
        aws ecs update-service --cluster coworkflow-cluster --service ms-usuarios-service --force-new-deployment
    # -------------------------------------------
```

**Nota:** Para cada microsserviço, você terá um bloco "Build and Push" e um comando "Update ECS Service" correspondentes. Certifique-se de que os nomes dos serviços no ECS (`ms-usuarios-service`) coincidam com o que você criou na AWS.
