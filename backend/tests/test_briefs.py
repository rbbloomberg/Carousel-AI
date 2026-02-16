"""Brief CRUD endpoint tests."""

import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_create_brief(client, test_user):
    _, _, token = test_user
    resp = await client.post(
        "/api/v1/briefs",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Summer Campaign",
            "campaign_objective": "Brand Awareness",
            "budget_total": 5000.0,
            "budget_duration_days": 30,
            "platforms": ["meta"],
            "kpis": ["CTR", "ROAS"],
            "brand_voice": "Friendly and professional",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Summer Campaign"
    assert data["status"] == "draft"
    assert data["platforms"] == ["meta"]


@pytest.mark.asyncio
async def test_list_briefs(client, test_user):
    _, _, token = test_user
    headers = {"Authorization": f"Bearer {token}"}

    # Create two briefs
    for title in ["Brief A", "Brief B"]:
        await client.post(
            "/api/v1/briefs",
            headers=headers,
            json={"title": title, "campaign_objective": "Traffic"},
        )

    resp = await client.get("/api/v1/briefs", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_submit_brief(client, test_user):
    _, _, token = test_user
    headers = {"Authorization": f"Bearer {token}"}

    # Create brief
    create_resp = await client.post(
        "/api/v1/briefs",
        headers=headers,
        json={"title": "Submit Test", "campaign_objective": "Sales"},
    )
    brief_id = create_resp.json()["id"]

    # Submit it (mock the Celery task)
    with patch("app.api.v1.briefs.run_campaign_pipeline") as mock_task:
        mock_task.delay.return_value = None
        resp = await client.post(
            f"/api/v1/briefs/{brief_id}/submit", headers=headers
        )

    assert resp.status_code == 200
    assert resp.json()["status"] == "submitted"
    mock_task.delay.assert_called_once_with(brief_id)
