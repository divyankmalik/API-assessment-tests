from flask import Blueprint, jsonify, request

from ..services import item_service
from ..validation import validate_item_changes, validate_new_item

bp = Blueprint("items", __name__, url_prefix="/api/items")


@bp.get("")
def list_items():
    args = request.args
    result = item_service.list_items(
        page=args.get("page"),
        limit=args.get("limit"),
        search=args.get("search"),
        category=args.get("category"),
    )
    return jsonify(result)


@bp.get("/stats")
def stats():
    return jsonify(item_service.get_stats())


@bp.get("/<item_id>")
def get_item(item_id):
    return jsonify(item_service.get_item(item_id))


@bp.post("")
def create_item():
    data = request.get_json(silent=True) or {}
    validate_new_item(data)
    item = item_service.create_item(data)
    return jsonify(item), 201


@bp.patch("/<item_id>")
def update_item(item_id):
    data = request.get_json(silent=True) or {}
    validate_item_changes(data)
    return jsonify(item_service.update_item(item_id, data))


@bp.delete("/<item_id>")
def delete_item(item_id):
    item_service.delete_item(item_id)
    return "", 204
