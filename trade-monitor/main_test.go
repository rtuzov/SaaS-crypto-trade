package main

import (
	"testing"
	"time"

	"github.com/IBM/sarama"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type MockConsumer struct {
	mock.Mock
}

func (m *MockConsumer) ConsumePartition(topic string, partition int32, offset int64) (sarama.PartitionConsumer, error) {
	args := m.Called(topic, partition, offset)
	return args.Get(0).(sarama.PartitionConsumer), args.Error(1)
}

func (m *MockConsumer) Close() error {
	args := m.Called()
	return args.Error(0)
}

type MockPartitionConsumer struct {
	mock.Mock
	messages chan *sarama.ConsumerMessage
	errors   chan *sarama.ConsumerError
}

func (m *MockPartitionConsumer) Messages() <-chan *sarama.ConsumerMessage {
	return m.messages
}

func (m *MockPartitionConsumer) Errors() <-chan *sarama.ConsumerError {
	return m.errors
}

func (m *MockPartitionConsumer) Close() error {
	args := m.Called()
	return args.Error(0)
}

func TestNewTradeMonitor(t *testing.T) {
	config := NewConfig()
	monitor, err := NewTradeMonitor(config)

	assert.NoError(t, err)
	assert.NotNil(t, monitor)
	assert.NotNil(t, monitor.logger)
	assert.NotNil(t, monitor.done)
}

func TestTradeMonitorSetup(t *testing.T) {
	config := NewConfig()
	monitor, _ := NewTradeMonitor(config)

	err := monitor.setup()

	assert.NoError(t, err)
	assert.NotNil(t, monitor.consumer)
	assert.NotNil(t, monitor.db)
}

func TestTradeMonitorProcessTrade(t *testing.T) {
	config := NewConfig()
	monitor, _ := NewTradeMonitor(config)

	tradeData := []byte(`{"user_id": "test_user", "symbol": "BTC/USDT", "side": "buy", "size": 1.0}`)

	err := monitor.processTrade(tradeData)

	assert.NoError(t, err)
}

func TestTradeMonitorCleanup(t *testing.T) {
	config := NewConfig()
	monitor, _ := NewTradeMonitor(config)

	mockConsumer := new(MockConsumer)
	mockConsumer.On("Close").Return(nil)

	monitor.consumer = mockConsumer
	monitor.cleanup()

	mockConsumer.AssertExpectations(t)
}

func TestTradeMonitorRun(t *testing.T) {
	config := NewConfig()
	monitor, _ := NewTradeMonitor(config)

	mockConsumer := new(MockConsumer)
	mockPartitionConsumer := &MockPartitionConsumer{
		messages: make(chan *sarama.ConsumerMessage, 1),
		errors:   make(chan *sarama.ConsumerError, 1),
	}

	mockConsumer.On("ConsumePartition", config.KafkaTopicTrades, int32(0), sarama.OffsetNewest).
		Return(mockPartitionConsumer, nil)

	monitor.consumer = mockConsumer

	// Send test message
	mockPartitionConsumer.messages <- &sarama.ConsumerMessage{
		Value: []byte(`{"user_id": "test_user", "symbol": "BTC/USDT", "side": "buy", "size": 1.0}`),
	}

	// Close done channel after a short delay
	go func() {
		time.Sleep(100 * time.Millisecond)
		close(monitor.done)
	}()

	err := monitor.run()

	assert.NoError(t, err)
	mockConsumer.AssertExpectations(t)
}
