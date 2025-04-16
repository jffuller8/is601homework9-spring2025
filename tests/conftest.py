import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_for_access_token(client):
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    response = await client.post("/token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_create_qr_code_unauthorized(client):
    # Attempt to create a QR code without authentication
    qr_request = {
        "url": "https://example.com",
        "size": 10,
    }
    response = await client.post("/qr_code", json=qr_request)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_and_delete_qr_code(client):
    # First, get the access token
    form_data = {
        "username": "admin",
        "password": "secret",
    }
    token_response = await client.post("/token", data=form_data)
    access_token = token_response.json()["access_token"]

    # Create a QR code
    qr_request = {
        "url": "https://example.com",
        "size": 10,
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    create_response = await client.post("/qr_code", json=qr_request, headers=headers)
    assert create_response.status_code == 200
    qr_code_id = create_response.json()["id"]

    # Delete the QR code
    delete_response = await client.delete(f"/qr_code/{qr_code_id}", headers=headers)
    assert delete_response.status_code == 200