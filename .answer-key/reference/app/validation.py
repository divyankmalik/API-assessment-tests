from .errors import HttpError

ALLOWED_FIELDS = {"name", "category", "price", "quantity"}


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _check_name(name):
    if not isinstance(name, str) or not name.strip():
        raise HttpError(400, "name is required")


def _check_price(price):
    if not _is_number(price) or price < 0:
        raise HttpError(400, "price must be a non-negative number")


def _check_quantity(quantity):
    if not _is_int(quantity) or quantity < 0:
        raise HttpError(400, "quantity must be a non-negative integer")


def validate_new_item(data):
    _check_name(data.get("name"))
    _check_price(data.get("price"))
    _check_quantity(data.get("quantity"))


def validate_item_changes(data):
    if not data:
        raise HttpError(400, "no fields to update")

    unknown = set(data) - ALLOWED_FIELDS
    if unknown:
        raise HttpError(400, f"unknown fields: {', '.join(sorted(unknown))}")

    if "name" in data:
        _check_name(data["name"])
    if "price" in data:
        _check_price(data["price"])
    if "quantity" in data:
        _check_quantity(data["quantity"])
