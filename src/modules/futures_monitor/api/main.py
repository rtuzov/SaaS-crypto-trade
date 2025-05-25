from fastapi import FastAPI
from .routes import router
import uvicorn
import os

app = FastAPI(title="Futures Monitor API")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    ) 