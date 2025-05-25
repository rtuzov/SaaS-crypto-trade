---
description: Python 3.11 + Go 1.22 micro-services
globs:
  - "**/*.py"
  - "**/*.go"
---

- Python использует **async FastAPI**; все модели = Pydantic v2.  
- **structlog** вместо `print()`; уровни debug > info > warning > error.  
- Kafka-топики kebab-case (`signals.user`).  
- Каждая корневая директория сервиса:  

main.py   # entry
app/      # бизнес-логика
adapters/ # Binance, Telegram…
tests/

- Минимум 80 % покрытия `pytest --cov`. 