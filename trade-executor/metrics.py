from prometheus_client import Counter, Gauge, Histogram
import time

# Метрики для торговых операций
trade_executions = Counter(
    'trade_executions_total',
    'Total number of trade executions',
    ['symbol', 'side', 'status']
)

trade_latency = Histogram(
    'trade_execution_latency_seconds',
    'Trade execution latency in seconds',
    ['symbol']
)

active_trades = Gauge(
    'active_trades',
    'Number of active trades',
    ['symbol', 'side']
)

trade_pnl = Gauge(
    'trade_pnl',
    'Current PnL for trades',
    ['symbol', 'side']
)

# Метрики для баланса
account_balance = Gauge(
    'account_balance',
    'Current account balance',
    ['currency']
)

margin_ratio = Gauge(
    'margin_ratio',
    'Current margin ratio',
    ['currency']
)

# Метрики для Kafka
kafka_messages_sent = Counter(
    'kafka_messages_sent_total',
    'Total number of messages sent to Kafka',
    ['topic']
)

kafka_message_latency = Histogram(
    'kafka_message_latency_seconds',
    'Kafka message processing latency in seconds',
    ['topic']
)

# Метрики для ошибок
trade_errors = Counter(
    'trade_errors_total',
    'Total number of trade execution errors',
    ['error_type']
)

# Метрики для Prometheus
TRADE_PROCESSING_TIME = Histogram(
    'trade_processing_seconds',
    'Time spent processing trade',
    ['symbol', 'side']
)

TRADE_PROCESSING_ERRORS = Counter(
    'trade_processing_errors_total',
    'Total number of trade processing errors',
    ['error_type']
)

TRADE_VOLUME = Counter(
    'trade_volume_total',
    'Total trading volume',
    ['symbol', 'side']
)

# Метрики для Kafka
KAFKA_MESSAGES_PROCESSED = Counter(
    'kafka_messages_processed_total',
    'Total number of Kafka messages processed',
    ['topic']
)

KAFKA_CONSUMER_LAG = Gauge(
    'kafka_consumer_lag',
    'Kafka consumer lag',
    ['topic', 'partition']
)

# Метрики для базы данных
DB_QUERY_TIME = Histogram(
    'db_query_seconds',
    'Time spent executing database queries',
    ['query_type']
)

DB_CONNECTION_ERRORS = Counter(
    'db_connection_errors_total',
    'Total number of database connection errors'
)

# Метрики для API
API_REQUEST_TIME = Histogram(
    'api_request_seconds',
    'Time spent processing API requests',
    ['endpoint', 'method']
)

API_ERRORS = Counter(
    'api_errors_total',
    'Total number of API errors',
    ['endpoint', 'status_code']
)

# Декоратор для измерения латентности
def measure_latency(metric):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                metric.observe(time.time() - start_time)
                return result
            except Exception as e:
                trade_errors.labels(error_type=type(e).__name__).inc()
                raise
        return wrapper
    return decorator 