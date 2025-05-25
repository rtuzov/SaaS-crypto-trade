from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class Position(BaseModel):
    symbol: str
    side: str
    entry_price: Decimal
    current_price: Decimal
    size: Decimal
    leverage: int
    pnl: Decimal
    pnl_percentage: Decimal
    liquidation_price: Decimal
    timestamp: datetime

class PositionUpdate(BaseModel):
    symbol: str
    current_price: Decimal
    pnl: Decimal
    pnl_percentage: Decimal
    timestamp: datetime

class UserPositions(BaseModel):
    user_id: str
    positions: List[Position]
    total_pnl: Decimal
    total_pnl_percentage: Decimal
    last_update: datetime

class MonitorSettings(BaseModel):
    user_id: str
    update_interval: int = Field(default=5, ge=1, le=60)  # seconds
    alert_threshold: Decimal = Field(default=Decimal('0.05'), ge=0, le=1)  # 5%
    enabled: bool = True 