---
description: Combined cursor rules for repo
globs: ["**/*"]
---

# Общие правила

- **English comments only**, UI-copy идёт через i18n JSON.  
- **kebab-case** для директорий/файлов; env-переменные UPPER_SNAKE.  
- Каждый TODO содержит действие и дату: `// TODO: refactor by 2025-05-30`.  
- Коммиты следуют Conventional Commits: `feat:`, `fix:`…  
- Любая новая зависимость → в PR-описании «почему она нужна».  

# Опасные команды

- Если команда начинается с **`sql.query`** и содержит `DROP` или `DELETE` → «ARE YOU SURE?»  
- `docker.rm*` и `docker.restart*` требуют подтверждения.  
- `workflow.terminate*` в Temporal → подтверждение.  
- Любые Refund/Cancel в Stripe/BTCPay → подтверждение и maxCostUSD = 1000. 