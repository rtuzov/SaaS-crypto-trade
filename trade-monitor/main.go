package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	"time"

	"github.com/IBM/sarama"
	"github.com/go-redis/redis/v8"
	"go.uber.org/zap"
)

type TradeEvent struct {
	UserID  string  `json:"user_id"`
	Symbol  string  `json:"symbol"`
	Side    string  `json:"side"`
	Size    float64 `json:"size"`
	Status  string  `json:"status"`
	OrderID string  `json:"order_id"`
	Price   float64 `json:"price"`
	Error   string  `json:"error,omitempty"`
}

type MonitoringConfig struct {
	MaxDrawdown       float64 `json:"max_drawdown"`
	StopLossPercent   float64 `json:"stop_loss_percent"`
	TakeProfitPercent float64 `json:"take_profit_percent"`
	MaxOpenTrades     int     `json:"max_open_trades"`
}

type TradeMonitor struct {
	config   *Config
	logger   *zap.Logger
	consumer sarama.Consumer
	db       *sql.DB
	done     chan struct{}
}

func NewTradeMonitor(config *Config) (*TradeMonitor, error) {
	logger, err := setupLogger(config)
	if err != nil {
		return nil, err
	}

	return &TradeMonitor{
		config: config,
		logger: logger,
		done:   make(chan struct{}),
	}, nil
}

func (tm *TradeMonitor) setup() error {
	// Setup Kafka consumer
	config := sarama.NewConfig()
	config.Consumer.Return.Errors = true

	consumer, err := sarama.NewConsumer([]string{tm.config.KafkaBootstrapServers}, config)
	if err != nil {
		return err
	}
	tm.consumer = consumer

	// Setup database connection
	db, err := sql.Open("postgres", tm.config.DatabaseURL())
	if err != nil {
		return err
	}
	tm.db = db

	// Test database connection
	if err := tm.db.Ping(); err != nil {
		return err
	}

	tm.logger.Info("Setup completed successfully")
	return nil
}

func (tm *TradeMonitor) processTrade(tradeData []byte) error {
	tm.logger.Info("Processing trade", zap.String("data", string(tradeData)))
	// Add your trade processing logic here
	return nil
}

func (tm *TradeMonitor) run() error {
	if err := tm.setup(); err != nil {
		return err
	}

	partitionConsumer, err := tm.consumer.ConsumePartition(tm.config.KafkaTopicTrades, 0, sarama.OffsetNewest)
	if err != nil {
		return err
	}
	defer partitionConsumer.Close()

	tm.logger.Info("Trade monitor started")

	for {
		select {
		case msg := <-partitionConsumer.Messages():
			if err := tm.processTrade(msg.Value); err != nil {
				tm.logger.Error("Error processing trade", zap.Error(err))
			}
		case err := <-partitionConsumer.Errors():
			tm.logger.Error("Kafka error", zap.Error(err))
		case <-tm.done:
			return nil
		}
	}
}

func (tm *TradeMonitor) cleanup() {
	if tm.consumer != nil {
		tm.consumer.Close()
	}
	if tm.db != nil {
		tm.db.Close()
	}
	tm.logger.Info("Cleanup completed")
}

func main() {
	config := NewConfig()
	monitor, err := NewTradeMonitor(config)
	if err != nil {
		panic(err)
	}

	// Healthcheck HTTP сервер
	go startHealthCheckServer()

	// Handle graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-sigChan
		monitor.logger.Info("Shutdown signal received")
		close(monitor.done)
	}()

	if err := monitor.run(); err != nil {
		monitor.logger.Fatal("Fatal error", zap.Error(err))
	}

	monitor.cleanup()
}

func getUserMonitoringConfig(rdb *redis.Client, userID string) (*MonitoringConfig, error) {
	ctx := context.Background()
	configJSON, err := rdb.Get(ctx, fmt.Sprintf("monitoring_config:%s", userID)).Result()
	if err == redis.Nil {
		// Возвращаем дефолтную конфигурацию
		return &MonitoringConfig{
			MaxDrawdown:       0.1,
			StopLossPercent:   0.05,
			TakeProfitPercent: 0.1,
			MaxOpenTrades:     5,
		}, nil
	}
	if err != nil {
		return nil, err
	}

	var config MonitoringConfig
	if err := json.Unmarshal([]byte(configJSON), &config); err != nil {
		return nil, err
	}
	return &config, nil
}

func checkMonitoringConditions(event TradeEvent, config *MonitoringConfig) error {
	// Проверка статуса сделки
	if event.Status == "error" {
		return fmt.Errorf("trade execution error: %s", event.Error)
	}

	// Проверка максимальной просадки
	if event.Side == "sell" {
		drawdown := (event.Price - event.Price*0.95) / event.Price
		if drawdown > config.MaxDrawdown {
			return fmt.Errorf("drawdown exceeds maximum allowed: %.2f%%", drawdown*100)
		}
	}

	// Проверка стоп-лосса
	if event.Side == "buy" {
		stopLoss := event.Price * (1 - config.StopLossPercent)
		if event.Price < stopLoss {
			return fmt.Errorf("stop loss triggered at price %.2f", event.Price)
		}
	}

	// Проверка тейк-профита
	if event.Side == "buy" {
		takeProfit := event.Price * (1 + config.TakeProfitPercent)
		if event.Price > takeProfit {
			return fmt.Errorf("take profit triggered at price %.2f", event.Price)
		}
	}

	return nil
}

func sendAlert(userID string, message string) {
	// TODO: Реализовать отправку уведомлений
	log.Printf("Alert for user %s: %s", userID, message)
}

func monitorServices() {
	services := []string{
		"trade-executor",
		"trade-monitor",
		"historical-analytics",
		"telegram-collector",
	}

	for {
		for _, service := range services {
			// Проверка статуса сервиса
			cmd := exec.Command("pgrep", "-f", service)
			err := cmd.Run()
			if err != nil {
				errorMsg := fmt.Sprintf("Service %s is down", service)
				log.Printf("ERROR: %s", errorMsg)
				sendAlert("system", errorMsg)

				// Попытка перезапуска сервиса
				restartCmd := exec.Command("systemctl", "restart", service)
				if restartErr := restartCmd.Run(); restartErr != nil {
					log.Printf("ERROR: Failed to restart service %s: %v", service, restartErr)
				}
			}
		}
		time.Sleep(30 * time.Second) // Увеличиваем интервал проверки
	}
}
