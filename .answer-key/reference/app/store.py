"""In-memory data store. Stands in for a real database."""

import copy

SEED = [
    {"id": 1, "name": "Widget", "category": "hardware", "price": 2.50, "quantity": 100},
    {"id": 2, "name": "Gadget", "category": "electronics", "price": 12.99, "quantity": 25},
    {"id": 3, "name": "Stapler", "category": "office", "price": 7.25, "quantity": 40},
    {"id": 4, "name": "Mini Widget", "category": "hardware", "price": 1.75, "quantity": 8},
    {"id": 5, "name": "USB Cable", "category": "electronics", "price": 4.99, "quantity": 150},
    {"id": 6, "name": "Notebook", "category": "office", "price": 3.10, "quantity": 10},
    {"id": 7, "name": "Hex Bolt", "category": "hardware", "price": 0.20, "quantity": 500},
    {"id": 8, "name": "Desk Lamp", "category": "electronics", "price": 24.00, "quantity": 5},
    {"id": 9, "name": "Sticky Notes", "category": "office", "price": 1.50, "quantity": 0},
    {"id": 10, "name": "Power Drill", "category": "hardware", "price": 89.99, "quantity": 12},
    {"id": 11, "name": "Monitor Stand", "category": "office", "price": 32.50, "quantity": 3},
    {"id": 12, "name": "HDMI Adapter", "category": "electronics", "price": 9.99, "quantity": 30},
]

_items = []
_next_id = 1


def reset():
    """Restore the store to the seed data. Called on startup and before every test."""
    global _items, _next_id
    _items = copy.deepcopy(SEED)
    _next_id = max(item["id"] for item in _items) + 1


def get_all():
    """Return a shallow copy of all items so callers can't reorder the store by accident."""
    return list(_items)


def next_id():
    global _next_id
    new_id = _next_id
    _next_id += 1
    return new_id


def insert(item):
    _items.append(item)


def replace(item):
    for index, existing in enumerate(_items):
        if existing["id"] == item["id"]:
            _items[index] = item
            return


def remove_at(index):
    return _items.pop(index)


reset()
