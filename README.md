# Message Persistence Service & Chat AI

## Overview

This project consists of two components:

1. **Message Persistence Service (app)**  
   - A Python FastAPI service that persists AI and user messages in a PostgreSQL database.
   - Provides endpoints to create, update, and retrieve messages.
   - Secured via API key.

2. **Chat AI Service (chat)**  
   - A separate Python FastAPI service that acts as a chat interface to an LLM (OpenAI `gpt-4o-mini`).
   - Sends messages to the persistence service for storage.
   - Retrieves message history for context/memory.

This setup uses Docker and Docker Compose for containerization and networking.
Since there is no UI I strongly advise usage of swagger interface available on `/docs`.
---

## Persistence Service

### Features

- Stores messages in PostgreSQL.
- Endpoints:
  - `POST /messages/` - create a new message.
  - `PUT /messages/{message_id}` - update an existing message.
  - `GET /messages/` - retrieve all messages.
- Secured via `x-api-key` header.
- Message schema:

```json
{
  "message_id": "UUID4",
  "chat_id": "UUID4",
  "content": "string",
  "rating": "true|false|null",
  "sent_at": "ISO8601 datetime string",
  "role": "ai|human"
}
```

### Running the App

```bash
    docker network create app_network
    docker compose -f docker-compose.yaml up --build
```

The service will be available on `http://localhost:8000`.

### API Key and DB password

Set the API key in `secrets/api_key.txt` and Docker Compose will mount it as `API_KEY`.
Set the DB password in secrets/db_password.txt
---

## Chat AI Service

### Features

* Provides `/chat` endpoint for sending messages to the AI.
* Uses the persistence service for storing messages.
* Retrieves message history to provide context to the AI.
* Uses OpenAI API key stored in Docker secrets.

### Running Chat Service Alone

```bash
  docker network create app_network
  docker compose -f docker-compose.chat.yaml up --build
```

The chat service will be available on `http://localhost:8100`.
Again I advise using `/docs`.

### Configuration

* OpenAI API key is provided via secret `secrets/openai_api_key.txt`.
* Persistence API base URL is set via `API_BASE_URL` environment variable (default: `http://app:8000`).

---

## Running Both Services Together

Make sure both Docker Compose files share the same external network (`app_network`):

```bash
    docker network create app_network
    docker compose -f docker-compose.yaml -f docker-compose.chat.yaml up --build
```

* Persistence service runs on port `8000`.
* Chat service runs on port `8100`.
* Messages sent via chat are persisted automatically in the database.

---

## Project Structure

```
.
├── app/                  # Persistence service
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── crud.py
│   ├── schemas.py
│   ├── database.py
│   ├── dependencies.py
│   └── config.py 
├── app_chat/            # Chat AI service
│   ├── __init__.py
│   ├── main.py
│   ├── chat.py
│   └── config.py
├── Dockerfile            # For persistence service
├── Dockerfile.chat       # For chat service
├── docker-compose.yaml
├── docker-compose.chat.yaml
├── requirements.txt
├── README.md
├── wait-for-it.sh        # Handles the timeout needed for the db to boot up
└── secrets/
│   ├── api_key.txt
│   ├── db_password.txt
│   └── openai_api_key.txt
│    
├── tests/               # Some basic tests that validate message persistance
│   ├── test_main.py
│   └── conftest.py
```

---

## Notes

* Both services are fully containerized.
* Persistence service validates UUIDs and ISO8601 datetimes.
* Chat service automatically handles message storage and retrieval.
* API keys are handled securely via Docker secrets.
* This project builds on the original Python Backend Engineer assignment, with an added chat interface for demonstration purposes.

---

