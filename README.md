# FastAPI Async
- Backend: FastAPI
- Fronted: Streamlit
- Database: PostgreSQL
- Message Broker: Redis Pub/Sub

## Run Docker Compose
```shell
docker compose up -d
```

## APIs
### Document
- http://127.0.0.1:8000/docs

### User
- GET /users
  - 전체 사용자 조회 
- POST /users/sign-up
  - 회원가입 
- POST /users/login
  - 로그인 

### Chat
- GET /chat-rooms
  - 새로운 1:1 채팅방 생성 
- POST /chat-rooms
  - 자신의 채팅방 목록 조회  
- GET /chat-rooms/{room-id}/message
  - 이전 대화 내역 조회 

### WebSocket
- /ws/chat-rooms/{room-id}
  - 실시간 채팅

## Run Test
```shell
pytest
```