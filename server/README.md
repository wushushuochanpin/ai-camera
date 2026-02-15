# AI Camera Server

FastAPI 后端（开发联调骨架）。

## Dev（Docker Compose）

在仓库根目录：

```bash
docker compose up --build
```

- Health: `GET http://localhost:8000/healthz`
- OpenAPI: `GET http://localhost:8000/docs`

## API
- `GET /v1/styles`
- `POST /v1/guidance`
- `WS /v1/guidance/ws`

> 注意：当前 `generate_guidance()` 为规则 stub，用于端到端联调；后续替换为真实推理服务。
