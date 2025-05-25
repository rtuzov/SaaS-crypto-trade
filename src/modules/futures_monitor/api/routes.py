from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.schemas import Position, UserPositions, MonitorSettings
from ..core.monitor import FuturesMonitor
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime

router = APIRouter(prefix="/api/v1/futures-monitor")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Global monitor instance
monitor = FuturesMonitor()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/start")
async def start_monitoring(
    settings: MonitorSettings,
    user_id: str = Depends(get_current_user)
):
    settings.user_id = user_id
    await monitor.start_monitoring(user_id, settings)
    return {"status": "success", "message": "Monitoring started"}

@router.post("/stop")
async def stop_monitoring(user_id: str = Depends(get_current_user)):
    await monitor.stop_monitoring(user_id)
    return {"status": "success", "message": "Monitoring stopped"}

@router.get("/positions", response_model=UserPositions)
async def get_positions(user_id: str = Depends(get_current_user)):
    positions = monitor.get_user_positions(user_id)
    if not positions:
        raise HTTPException(status_code=404, detail="No positions found")
    return positions

@router.get("/positions/all", response_model=List[UserPositions])
async def get_all_positions(user_id: str = Depends(get_current_user)):
    # TODO: Check if user has admin rights
    return list(monitor.get_all_positions().values())

@router.get("/settings", response_model=MonitorSettings)
async def get_settings(user_id: str = Depends(get_current_user)):
    settings = monitor.settings.get(user_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

@router.put("/settings")
async def update_settings(
    settings: MonitorSettings,
    user_id: str = Depends(get_current_user)
):
    settings.user_id = user_id
    monitor.settings[user_id] = settings
    return {"status": "success", "message": "Settings updated"} 