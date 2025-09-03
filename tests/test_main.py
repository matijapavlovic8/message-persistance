import os
import uuid
from datetime import datetime, UTC

def get_secret(name: str) -> str:
    file_path = "/run/secrets/api_key"
    if file_path and os.path.exists(file_path):
        with open(file_path) as f:
            return f.read().strip()
    raise ValueError(f"Secret {name} not found")

print(get_secret("API_KEY"))

def auth_headers():
    return {"X-API-Key": get_secret("API_KEY")}

def test_create_message(client):
    sample_message = {
        "chat_id": str(uuid.uuid4()),
        "content": "Hello world",
        "rating": True,
        "sent_at": datetime.now(UTC).isoformat(),
        "role": "user",
    }

    response = client.post("/messages/", json=sample_message, headers=auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Hello world"
    assert data["role"] == "user"
    assert "message_id" in data


def test_update_message(client):
    create_response = client.post(
        "/messages/",
        json={
            "chat_id": str(uuid.uuid4()),
            "content": "Message to update",
            "rating": False,
            "sent_at": datetime.now(UTC).isoformat(),
            "role": "user",
        },
        headers=auth_headers(),
    )
    assert create_response.status_code == 200
    message_id = create_response.json()["message_id"]

    response = client.put(
        f"/messages/{message_id}",
        json={"content": "Updated content"},
        headers=auth_headers(),
    )
    assert response.status_code == 200
    assert response.json()["content"] == "Updated content"


def test_get_messages(client):
    client.post(
        "/messages/",
        json={
            "chat_id": str(uuid.uuid4()),
            "content": "Fetch me",
            "rating": True,
            "sent_at": datetime.now(UTC).isoformat(),
            "role": "user",
        },
        headers=auth_headers(),
    )

    response = client.get("/messages/", headers=auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(msg["content"] == "Fetch me" for msg in data)


def test_unauthorized(client):
    response = client.get("/messages/")
    assert response.status_code == 401
