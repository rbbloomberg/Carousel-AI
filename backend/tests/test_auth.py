"""Auth endpoint tests."""

import pytest


@pytest.mark.asyncio
async def test_register(client):
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@example.com",
            "password": "securepass123",
            "full_name": "New User",
            "company_name": "New Corp",
            "industry": "ecommerce",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "email": "dup@example.com",
        "password": "securepass123",
        "full_name": "Dup User",
        "company_name": "Dup Corp",
    }
    resp1 = await client.post("/api/v1/auth/register", json=payload)
    assert resp1.status_code == 201

    resp2 = await client.post("/api/v1/auth/register", json=payload)
    assert resp2.status_code == 400


@pytest.mark.asyncio
async def test_login(client, test_user):
    user, _, _ = test_user
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpass123"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client, test_user):
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrong"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client, test_user):
    _, _, token = test_user
    resp = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
