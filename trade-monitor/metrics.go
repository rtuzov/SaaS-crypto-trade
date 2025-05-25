package main

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    // Метрики для мониторинга сервисов
    serviceHealth = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "service_health",
            Help: "Health status of services (1 = healthy, 0 = unhealthy)",
        },
        []string{"service"},
    )

    serviceUptime = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "service_uptime_seconds",
            Help: "Service uptime in seconds",
        },
        []string{"service"},
    )

    // Метрики для торговых операций
    tradeProcessingTime = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name: "trade_processing_seconds",
            Help: "Time spent processing trade",
        },
        []string{"symbol", "side"},
    )

    tradeProcessingErrors = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "trade_processing_errors_total",
            Help: "Total number of trade processing errors",
        },
        []string{"error_type"},
    )

    tradeVolume = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "trade_volume_total",
            Help: "Total trading volume",
        },
        []string{"symbol", "side"},
    )

    activeTrades = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "active_trades",
            Help: "Number of active trades",
        },
        []string{"symbol"},
    )

    // Метрики для Kafka
    kafkaConsumerLag = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "kafka_consumer_lag",
            Help: "Kafka consumer lag",
        },
        []string{"topic", "partition"},
    )

    kafkaMessagesProcessed = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "kafka_messages_processed_total",
            Help: "Total number of Kafka messages processed",
        },
        []string{"topic"},
    )

    // Метрики для алертов
    alertCount = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "alert_count_total",
            Help: "Total number of alerts generated",
        },
        []string{"severity", "type"},
    )

    // Метрики для производительности
    messageProcessingLatency = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "message_processing_latency_seconds",
            Help:    "Message processing latency in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"type"},
    )

    // Метрики для базы данных
    dbQueryTime = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name: "db_query_seconds",
            Help: "Time spent executing database queries",
        },
        []string{"query_type"},
    )

    dbConnectionErrors = promauto.NewCounter(
        prometheus.CounterOpts{
            Name: "db_connection_errors_total",
            Help: "Total number of database connection errors",
        },
    )

    // Метрики для API
    apiRequestTime = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name: "api_request_seconds",
            Help: "Time spent processing API requests",
        },
        []string{"endpoint", "method"},
    )

    apiErrors = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "api_errors_total",
            Help: "Total number of API errors",
        },
        []string{"endpoint", "status_code"},
    )
)

// Функции-помощники для обновления метрик
func updateServiceHealth(service string, healthy bool) {
    if healthy {
        serviceHealth.WithLabelValues(service).Set(1)
    } else {
        serviceHealth.WithLabelValues(service).Set(0)
    }
}

func updateServiceUptime(service string, uptime float64) {
    serviceUptime.WithLabelValues(service).Set(uptime)
}

func updateKafkaLag(group, topic string, lag float64) {
    kafkaConsumerLag.WithLabelValues(group, topic).Set(lag)
}

func incrementMessagesProcessed(topic string) {
    kafkaMessagesProcessed.WithLabelValues(topic).Inc()
}

func incrementAlertCount(severity, alertType string) {
    alertCount.WithLabelValues(severity, alertType).Inc()
} 