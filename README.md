# FastAPI Async
- Backend: FastAPI
- Database: PostgreSQL
- Message Broker: Redis Pub/Sub

## Run Server
### Docker Compose
```shell
docker compose up -d
```
### Sync Database
```shell
alembic upgrade head
```
### Run Test
```shell
pytest
```

### Run load test
1. Sync / 100 Connections / 10s
   - wrk -c 100 -d 10 http://127.0.0.1:8000/sync/sleep
2. ASync / 100 Connections / 10s
   - wrk -c 100 -d 10 http://127.0.0.1:8000/async/sleep
