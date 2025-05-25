import pytest
import json
from unittest.mock import Mock, patch
from main import TradeExecutor, TradeCommand

@pytest.fixture
def mock_kafka_consumer():
    with patch('main.Consumer') as mock:
        yield mock

@pytest.fixture
def mock_db_connection():
    with patch('main.psycopg2.connect') as mock:
        yield mock

@pytest.fixture
def trade_executor(mock_kafka_consumer, mock_db_connection):
    return TradeExecutor()

@pytest.mark.asyncio
async def test_setup(trade_executor):
    await trade_executor.setup()
    assert trade_executor.consumer is not None
    assert trade_executor.db_conn is not None

@pytest.mark.asyncio
async def test_process_trade(trade_executor):
    trade_data = {
        'user_id': 'test_user',
        'symbol': 'BTC/USDT',
        'side': 'buy',
        'size': 1.0
    }
    
    with patch('main.logger') as mock_logger:
        await trade_executor.process_trade(json.dumps(trade_data))
        mock_logger.info.assert_called_once()

@pytest.mark.asyncio
async def test_cleanup(trade_executor):
    trade_executor.consumer = Mock()
    trade_executor.db_conn = Mock()
    
    trade_executor.cleanup()
    
    trade_executor.consumer.close.assert_called_once()
    trade_executor.db_conn.close.assert_called_once()

@pytest.mark.asyncio
async def test_handle_shutdown(trade_executor):
    trade_executor.handle_shutdown(None, None)
    assert not trade_executor.running

@pytest.mark.asyncio
async def test_run_with_error(trade_executor, mock_kafka_consumer):
    mock_consumer = Mock()
    mock_consumer.poll.side_effect = Exception("Test error")
    trade_executor.consumer = mock_consumer
    
    with patch('main.logger') as mock_logger:
        await trade_executor.run()
        mock_logger.error.assert_called() 