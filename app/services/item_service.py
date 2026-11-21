from .. import store
from ..errors import HttpError
from ..pagination import paginate

LOW_STOCK_THRESHOLD = 10


def _parse_id(item_id):
    try:
        return int(item_id)
    except (TypeError, ValueError):
        raise HttpError(404, f"Item {item_id} not found")


def list_items(page=None, limit=None, search=None, category=None):
    items = store.get_all()

    if search:
        query = search.strip().lower()
        items = [item for item in items if query in item["name"].lower()]

    if category:
        items = [item for item in items if item["category"] == category]

    return paginate(items, page, limit)


def get_item(item_id):
    for item in store.get_all():
        if item["id"] == item_id:
            return item
            
    raise HttpError(404, f"Item {item_id} not found")


def create_item(data):
    item = {
        "id": store.next_id(),
        "name": data["name"].strip(),
        "category": data.get("category") or "general",
        "price": data["price"],
        "quantity": data["quantity"],
    }
    store.insert(item)
    return item


def update_item(item_id, changes):
    existing = get_item(item_id)

    updated = {**existing, **changes, "id": existing["id"]}
    if "name" in changes:
        updated["name"] = changes["name"].strip()

    store.replace(updated)
    return updated


def delete_item(item_id):
    item_id = _parse_id(item_id)
    index = next(
        (idx for idx,item in enumerate(store.get_all()) if item["id"] == item_id),
        -1,
    )
    if index == -1:
        raise HttpError(404, f"Item {item_id} not found")
    store.remove_at(index)



def get_stats():
    items = store.get_all()
    count = len(items)

    total_value = sum(item["price"] * item["quantity"] for item in items)
    average_price = sum(item["price"] for item in items) / count if count else 0

    return {
        "total_items": count,
        "total_units": sum(item["quantity"] for item in items),
        "total_value": round(total_value, 2),
        "average_price": round(average_price, 2),
        "low_stock": [
            item["name"] for item in items if item["quantity"] < LOW_STOCK_THRESHOLD
        ],
    }
