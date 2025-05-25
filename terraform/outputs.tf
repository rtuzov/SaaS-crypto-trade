output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "private_subnets" {
  description = "List of private subnet IDs"
  value       = module.vpc.private_subnets
}

output "public_subnets" {
  description = "List of public subnet IDs"
  value       = module.vpc.public_subnets
}

output "eks_cluster_name" {
  description = "Name of the EKS cluster"
  value       = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_security_group_id" {
  description = "Security group ID attached to the EKS cluster"
  value       = module.eks.cluster_security_group_id
}

output "eks_node_groups" {
  description = "Map of EKS node groups"
  value       = module.eks.eks_managed_node_groups
}

output "rds_endpoint" {
  description = "Endpoint of the RDS instance"
  value       = module.rds.db_instance_endpoint
}

output "rds_port" {
  description = "Port of the RDS instance"
  value       = module.rds.db_instance_port
}

output "rds_database_name" {
  description = "Name of the RDS database"
  value       = module.rds.db_instance_name
}

output "redis_endpoint" {
  description = "Endpoint of the Redis cluster"
  value       = module.elasticache.elasticache_replication_group_primary_endpoint_address
}

output "redis_port" {
  description = "Port of the Redis cluster"
  value       = module.elasticache.elasticache_replication_group_port
}

output "kafka_bootstrap_brokers" {
  description = "Bootstrap brokers for Kafka"
  value       = module.msk.bootstrap_brokers
}

output "kafka_bootstrap_brokers_tls" {
  description = "TLS bootstrap brokers for Kafka"
  value       = module.msk.bootstrap_brokers_tls
}

output "kafka_bootstrap_brokers_sasl_scram" {
  description = "SASL/SCRAM bootstrap brokers for Kafka"
  value       = module.msk.bootstrap_brokers_sasl_scram
}

output "kafka_bootstrap_brokers_iam" {
  description = "IAM bootstrap brokers for Kafka"
  value       = module.msk.bootstrap_brokers_iam
}

output "kafka_zookeeper_connection_string" {
  description = "Zookeeper connection string"
  value       = module.msk.zookeeper_connection_string
}

output "kafka_security_group_id" {
  description = "Security group ID for Kafka"
  value       = aws_security_group.kafka.id
}

output "redis_security_group_id" {
  description = "Security group ID for Redis"
  value       = aws_security_group.redis.id
}

output "rds_security_group_id" {
  description = "Security group ID for RDS"
  value       = aws_security_group.rds.id
} 