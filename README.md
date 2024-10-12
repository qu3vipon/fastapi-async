# FastAPI Async
- Backend: FastAPI
- Database: PostgreSQL
- Message Broker: Redis Pub/Sub

## Run Server
- Python 3.11+

### Install Packages
```shell
pip install -r src/requirements.txt
```

### Docker Compose
```shell
# run db & redis
docker compose up -d
docker compose down

# with servers
docker compose -f docker-compose.server.yml up -d
docker compose down --remove-orphans
```
### Run Migrations
```shell
alembic upgrade head
```
## Run Test
```shell
pytest
```

## Run load test
1. Sync / 100 Connections / 10s
   - wrk -c 100 -d 10 http://127.0.0.1:8000/sync/sleep
2. ASync / 100 Connections / 10s
   - wrk -c 100 -d 10 http://127.0.0.1:8000/async/sleep
