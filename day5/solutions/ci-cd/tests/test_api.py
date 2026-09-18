import pytest
import uuid

@pytest.mark.asyncio
async def test_create_and_retrieve_jsonb_item(client):
    # Test Postgres JSONB handling and UUID generation
    payload = {
        "name": "Production Payload",
        "metadata_payload": {"tier": "gold", "tags": ["backend", "db"]}
    }
    
    create_res = await client.post("/items", json=payload)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["name"] == "Production Payload"
    assert created_data["metadata_payload"]["tier"] == "gold"
    
    item_id = created_data["id"]
    
    get_res = await client.get(f"/items/{item_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == item_id

@pytest.mark.asyncio
async def test_multiple_items_are_independent(client):
    # verifies that two items get different UUIDs and retrieving one returns the correct item 
    payload1 = {"name": "Item A", "metadata_payload": {}}
    payload2 = {"name": "Item B", "metadata_payload": {}}

    res1 = await client.post("/items", json=payload1)
    res2 = await client.post("/items", json=payload2)

    id1 = res1.json()["id"]
    id2 = res2.json()["id"]

    assert id1 != id2

    get_res = await client.get(f"/items/{id1}")
    assert get_res.json()["name"] == "Item A"