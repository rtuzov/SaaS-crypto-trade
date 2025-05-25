package main

import (
	"fmt"
	"os"
	"strconv"
)

type Config struct {
	// Database
	DBHost     string
	DBPort     int
	DBName     string
	DBUser     string
	DBPassword string

	// Kafka
	KafkaBootstrapServers string
	KafkaConsumerGroup    string
	KafkaTopicTrades      string

	// Monitoring
	PrometheusPort int
	LogLevel       string
}

func (c *Config) DatabaseURL() string {
	return fmt.Sprintf("postgresql://%s:%s@%s:%d/%s?sslmode=disable",
		c.DBUser, c.DBPassword, c.DBHost, c.DBPort, c.DBName)
}

func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value, exists := os.LookupEnv(key); exists {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func NewConfig() *Config {
	return &Config{
		// Database
		DBHost:     getEnv("DB_HOST", "postgres"),
		DBPort:     getEnvInt("DB_PORT", 5432),
		DBName:     getEnv("DB_NAME", "trading"),
		DBUser:     getEnv("DB_USER", "postgres"),
		DBPassword: getEnv("DB_PASSWORD", "postgres123"),

		// Kafka
		KafkaBootstrapServers: getEnv("KAFKA_BOOTSTRAP_SERVERS", "redpanda:9092"),
		KafkaConsumerGroup:    getEnv("KAFKA_CONSUMER_GROUP", "trade-monitor"),
		KafkaTopicTrades:      getEnv("KAFKA_TOPIC_TRADES", "trades"),

		// Monitoring
		PrometheusPort: getEnvInt("PROMETHEUS_PORT", 8080),
		LogLevel:       getEnv("LOG_LEVEL", "info"),
	}
}
