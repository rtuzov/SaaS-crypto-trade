from datetime import timedelta
from temporalio import workflow, activity
from dataclasses import dataclass
from typing import Optional
import asyncpg
import os
from trade_executor.utils.binance import BinanceFuturesClient
import logging

logger = logging.getLogger(__name__)

@dataclass
class TradeInput:
    user_id: str
    symbol: str
    side: str
    amount: float
    leverage: int

@dataclass
class TradeResult:
    success: bool
    order_id: Optional[str] = None
    error: Optional[str] = None

async def get_db_connection():
    return await asyncpg.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        port=int(os.getenv('POSTGRES_PORT', 5432)),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'trading')
    )

async def get_user_api_keys(user_id: str) -> tuple[str, str]:
    conn = await get_db_connection()
    try:
        row = await conn.fetchrow(
            """
            SELECT api_key_enc 
            FROM core.user_api_keys 
            WHERE user_id = $1 AND exchange = 'binance'
            """,
            user_id
        )
        if not row:
            raise ValueError("API keys not found")
            
        # TODO: Decrypt api_key_enc using PGP_MASTER_KEY
        # For now, return dummy values
        return "dummy_key", "dummy_secret"
    finally:
        await conn.close()

@activity.defn
async def validate_balance(input: TradeInput) -> bool:
    try:
        api_key, api_secret = await get_user_api_keys(input.user_id)
        client = BinanceFuturesClient(api_key, api_secret)
        
        balance = await client.get_balance()
        required_margin = input.amount * input.leverage
        
        return balance['free'] >= required_margin
    except Exception as e:
        logger.error(f"Error validating balance: {e}")
        return False

@activity.defn
async def place_order(input: TradeInput) -> TradeResult:
    try:
        api_key, api_secret = await get_user_api_keys(input.user_id)
        client = BinanceFuturesClient(api_key, api_secret)
        
        order = await client.create_order(
            symbol=input.symbol,
            side=input.side,
            amount=input.amount,
            leverage=input.leverage
        )
        
        # Save order to database
        conn = await get_db_connection()
        try:
            await conn.execute(
                """
                INSERT INTO core.orders 
                (user_id, exchange_order_id, pair, side, leverage, amount, status)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                input.user_id,
                order['id'],
                input.symbol,
                input.side,
                input.leverage,
                input.amount,
                order['status']
            )
        finally:
            await conn.close()
            
        return TradeResult(
            success=True,
            order_id=order['id']
        )
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        return TradeResult(
            success=False,
            error=str(e)
        )

@activity.defn
async def cancel_order(order_id: str) -> bool:
    try:
        # Get order details from database
        conn = await get_db_connection()
        try:
            order = await conn.fetchrow(
                """
                SELECT user_id, pair 
                FROM core.orders 
                WHERE exchange_order_id = $1
                """,
                order_id
            )
            if not order:
                return False
                
            api_key, api_secret = await get_user_api_keys(order['user_id'])
            client = BinanceFuturesClient(api_key, api_secret)
            
            success = await client.cancel_order(order_id, order['pair'])
            
            if success:
                await conn.execute(
                    """
                    UPDATE core.orders 
                    SET status = 'closed' 
                    WHERE exchange_order_id = $1
                    """,
                    order_id
                )
                
            return success
        finally:
            await conn.close()
    except Exception as e:
        logger.error(f"Error canceling order: {e}")
        return False

@workflow.defn
class ExecuteTradeWorkflow:
    @workflow.run
    async def run(self, input: TradeInput) -> TradeResult:
        # Validate balance
        balance_valid = await workflow.execute_activity(
            validate_balance,
            input,
            start_to_close_timeout=timedelta(seconds=5)
        )
        
        if not balance_valid:
            return TradeResult(success=False, error="Insufficient balance")
        
        # Place order with retry
        try:
            result = await workflow.execute_activity(
                place_order,
                input,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy={
                    "maximum_attempts": 3,
                    "initial_interval": timedelta(seconds=1),
                    "maximum_interval": timedelta(seconds=10),
                    "backoff_coefficient": 2.0
                }
            )
            
            if not result.success:
                # Cancel order if placement failed
                await workflow.execute_activity(
                    cancel_order,
                    result.order_id,
                    start_to_close_timeout=timedelta(seconds=5)
                )
            
            return result
            
        except Exception as e:
            return TradeResult(success=False, error=str(e)) 