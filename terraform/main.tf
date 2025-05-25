terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }
  backend "s3" {
    bucket         = "trading-platform-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.environment
      Project     = "trading-platform"
      ManagedBy   = "terraform"
    }
  }
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args = [
      "eks",
      "get-token",
      "--cluster-name",
      module.eks.cluster_name
    ]
  }
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args = [
        "eks",
        "get-token",
        "--cluster-name",
        module.eks.cluster_name
      ]
    }
  }
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "trading-platform-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway     = true
  single_nat_gateway     = false
  one_nat_gateway_per_az = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Environment = var.environment
    Project     = "trading-platform"
  }
}

module "eks" {
  source = "terraform-aws-modules/eks/aws"

  cluster_name    = "trading-platform-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    general = {
      desired_size = 2
      min_size     = 1
      max_size     = 5

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"

      labels = {
        Environment = var.environment
        Project     = "trading-platform"
      }

      taints = []

      tags = {
        Environment = var.environment
        Project     = "trading-platform"
      }
    }
  }

  tags = {
    Environment = var.environment
    Project     = "trading-platform"
  }
}

module "rds" {
  source = "terraform-aws-modules/rds/aws"

  identifier = "trading-platform-${var.environment}"

  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.medium"
  allocated_storage = 20

  db_name  = "trading"
  username = var.db_username
  port     = "5432"

  vpc_security_group_ids = [aws_security_group.rds.id]
  subnet_ids             = module.vpc.private_subnets

  family = "postgres15"

  major_engine_version = "15"

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"

  backup_retention_period = 7
  skip_final_snapshot    = true

  performance_insights_enabled = true

  tags = {
    Environment = var.environment
    Project     = "trading-platform"
  }
}

module "elasticache" {
  source = "terraform-aws-modules/elasticache/aws"

  cluster_id           = "trading-platform-${var.environment}"
  engine              = "redis"
  engine_version      = "7.0"
  node_type           = "cache.t3.micro"
  num_cache_nodes     = 1
  port                = 6379
  subnet_ids          = module.vpc.private_subnets
  security_group_ids  = [aws_security_group.redis.id]

  tags = {
    Environment = var.environment
    Project     = "trading-platform"
  }
}

module "msk" {
  source = "terraform-aws-modules/msk/aws"

  cluster_name           = "trading-platform-${var.environment}"
  kafka_version         = "3.5.1"
  number_of_broker_nodes = 3

  broker_node_group_info = {
    instance_type   = "kafka.t3.small"
    ebs_storage_info = {
      volume_size = 100
    }
    client_subnets = module.vpc.private_subnets
    security_groups = [aws_security_group.kafka.id]
  }

  tags = {
    Environment = var.environment
    Project     = "trading-platform"
  }
}

resource "aws_security_group" "rds" {
  name        = "trading-platform-rds-${var.environment}"
  description = "Security group for RDS"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [module.eks.cluster_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = var.environment
    Project     = "trading-platform"
  }
}

resource "aws_security_group" "redis" {
  name        = "trading-platform-redis-${var.environment}"
  description = "Security group for Redis"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [module.eks.cluster_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = var.environment
    Project     = "trading-platform"
  }
}

resource "aws_security_group" "kafka" {
  name        = "trading-platform-kafka-${var.environment}"
  description = "Security group for Kafka"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 9092
    to_port         = 9092
    protocol        = "tcp"
    security_groups = [module.eks.cluster_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = var.environment
    Project     = "trading-platform"
  }
} 