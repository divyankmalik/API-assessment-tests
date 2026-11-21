"""API tests, grouped by feature."""

NEW_ITEM = {"name": "Laser Pointer", "category": "electronics", "price": 15.00, "quantity": 20}


class TestListItems:
    def test_default_list_returns_first_page(self, client):
        res = client.get("/api/items")
        assert res.status_code == 200
        body = res.get_json()
        assert body["total"] == 12
        assert body["page"] == 1
        assert [item["id"] for item in body["data"]] == list(range(1, 11))

    def test_search_is_case_insensitive(self, client):
        res = client.get("/api/items?search=WIDGET")
        names = [item["name"] for item in res.get_json()["data"]]
        assert names == ["Widget", "Mini Widget"]

    def test_filter_by_category(self, client):
        res = client.get("/api/items?category=office")
        assert {item["category"] for item in res.get_json()["data"]} == {"office"}


class TestGetItemById:
    def test_returns_existing_item(self, client):
        res = client.get("/api/items/3")
        assert res.status_code == 200
        assert res.get_json()["name"] == "Stapler"

    def test_missing_item_returns_404(self, client):
        res = client.get("/api/items/999")
        assert res.status_code == 404

    def test_non_numeric_id_returns_404(self, client):
        res = client.get("/api/items/abc")
        assert res.status_code == 404


class TestCreateItem:
    def test_create_returns_201_with_new_id(self, client):
        res = client.post("/api/items", json=NEW_ITEM)
        assert res.status_code == 201
        assert res.get_json()["id"] == 13

    def test_created_item_is_persisted(self, client):
        created = client.post("/api/items", json=NEW_ITEM).get_json()

        res = client.get(f"/api/items/{created['id']}")
        assert res.status_code == 200
        assert res.get_json()["name"] == "Laser Pointer"

        assert client.get("/api/items").get_json()["total"] == 13


class TestPagination:
    def test_second_page(self, client):
        res = client.get("/api/items?page=2&limit=5")
        assert [item["id"] for item in res.get_json()["data"]] == [6, 7, 8, 9, 10]

    def test_last_partial_page(self, client):
        res = client.get("/api/items?page=3&limit=5")
        body = res.get_json()
        assert [item["id"] for item in body["data"]] == [11, 12]
        assert body["total_pages"] == 3


class TestUpdateItem:
    def test_partial_update_keeps_other_fields(self, client):
        res = client.patch("/api/items/2", json={"price": 10.49})
        assert res.status_code == 200
        assert res.get_json() == {
            "id": 2,
            "name": "Gadget",
            "category": "electronics",
            "price": 10.49,
            "quantity": 25,
        }

    def test_update_is_persisted(self, client):
        client.patch("/api/items/2", json={"quantity": 99})
        item = client.get("/api/items/2").get_json()
        assert item["quantity"] == 99
        assert item["name"] == "Gadget"


class TestDeleteItem:
    def test_delete_existing_item(self, client):
        res = client.delete("/api/items/4")
        assert res.status_code == 204
        assert client.get("/api/items/4").status_code == 404
        assert client.get("/api/items").get_json()["total"] == 11

    def test_delete_missing_item_returns_404_and_changes_nothing(self, client):
        res = client.delete("/api/items/999")
        assert res.status_code == 404
        assert client.get("/api/items").get_json()["total"] == 12
        assert client.get("/api/items/12").status_code == 200


class TestValidation:
    def test_quantity_zero_is_allowed(self, client):
        res = client.post("/api/items", json={**NEW_ITEM, "quantity": 0})
        assert res.status_code == 201
        assert res.get_json()["quantity"] == 0

    def test_missing_name_returns_400(self, client):
        res = client.post("/api/items", json={"price": 1.0, "quantity": 1})
        assert res.status_code == 400
        assert "name" in res.get_json()["error"]

    def test_negative_price_returns_400(self, client):
        res = client.post("/api/items", json={**NEW_ITEM, "price": -5})
        assert res.status_code == 400

    def test_negative_quantity_returns_400(self, client):
        res = client.post("/api/items", json={**NEW_ITEM, "quantity": -1})
        assert res.status_code == 400

    def test_patch_unknown_field_returns_400(self, client):
        res = client.patch("/api/items/1", json={"colour": "red"})
        assert res.status_code == 400


class TestStats:
    def test_stats(self, client):
        res = client.get("/api/items/stats")
        assert res.status_code == 200
        assert res.get_json() == {
            "total_items": 12,
            "total_units": 883,
            "total_value": 3355.33,
            "average_price": 15.9,
            "low_stock": ["Mini Widget", "Desk Lamp", "Sticky Notes", "Monitor Stand"],
        }
