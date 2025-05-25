---
description: Commands that must ask confirmation
globs: ["**/*"]
mcpOnly: true
---

- Если команда начинается с **`sql.query`** и содержит `DROP` или `DELETE` → «ARE YOU SURE?»  
- `docker.rm*` и `docker.restart*` требуют подтверждения.  
- `workflow.terminate*` в Temporal → подтверждение.  
- Любые Refund/Cancel в Stripe/BTCPay → подтверждение и maxCostUSD = 1000.  

Cursor применяет эти bullet-правила на этапе «MCP-bridge». 