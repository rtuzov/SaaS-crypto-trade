---
description: Rules for backend services
globs: ["**/*.py", "**/*.go"]
---

# Backend Rules

- Python использует **async FastAPI**; все модели = Pydantic v2.  
- **structlog** вместо `print()`; уровни debug > info > warning > error.  
- Kafka-топики kebab-case (`signals.user`).  
- Каждая корневая директория сервиса:  

```
main.py   # entry
app/      # бизнес-логика
adapters/ # Binance, Telegram…
tests/
```

- Минимум 80 % покрытия `pytest --cov`. 