# ai-camera

iOS AI 人像相机（云端实时指导 + Pose 教练）。

## Repo 结构
- `server/`: 后端 API（FastAPI），用于实时指导与会话管理（开发模式支持热重载）
- `docs/`: 产品与接口文档
- iOS 工程：由 Xcode 创建后放在仓库根目录或 `ios/`（按团队约定调整）

## 后端本地开发（在开发服务器上）

```bash
cd server
# 在 repo 根目录运行
cd ..
docker compose up --build
```

- API: `http://localhost:8000`
- Health: `GET /healthz`
- OpenAPI: `GET /docs`

> 说明：该后端当前为“可联调的接口骨架”，AI 推理逻辑后续替换为实际模型服务。
