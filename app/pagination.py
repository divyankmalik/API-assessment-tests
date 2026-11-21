import math

DEFAULT_LIMIT = 10


def _to_positive_int(value, default):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return number if number > 0 else default


def paginate(items, page, limit):
    """Pages are 1-indexed: page=1 is the first page."""
    page = _to_positive_int(page, 1)
    limit = _to_positive_int(limit, DEFAULT_LIMIT)

    offset = (page - 1) * limit

    return {
        "data": items[offset:offset + limit],
        "page": page,
        "limit": limit,
        "total": len(items),
        "total_pages": math.ceil(len(items) / limit),
    }
