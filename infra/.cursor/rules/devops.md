---
description: Docker, Helm, GitHub Actions
globs:
  - "**/*.yml"
  - "**/*.yaml"
  - "**/Dockerfile"
---

- Docker образ – *multi-stage*; всегда USER `appuser` после COPY.  
- Все порты читаются из ENV или `.Values`; никаких `localhost:3000` в Dockerfile.  
- Helm `values.yaml` ключи camelCase.  
- GitHub Actions кеширует pip, npm, go modules.  
- k6-скрипты лежат в `infra/k6`, nightly-run файл в `.github/workflows/k6.yml`. 