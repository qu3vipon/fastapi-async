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