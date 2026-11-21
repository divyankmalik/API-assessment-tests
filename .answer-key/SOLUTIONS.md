# Answer key (spoilers)

11 bugs across 9 tickets. The full working code is in `reference/`. Run `diff -r app .answer-key/reference/app` to check your fixes.

## Suggested order and why

Fix **BUG-101 first**. While the error handler is broken, every `HttpError` (every 400 and 404) becomes a 500. That accounts for 7 of the 19 failing tests and hides the real symptoms of the other bugs. In the real round, look for the one root cause that cascades before you chase individual tests.

---

### BUG-101: Error handler reads the wrong attribute
`app/__init__.py`
```python
status = getattr(err, "status_code", 500)   # bug: HttpError defines .status, not .status_code
status = getattr(err, "status", 500)        # fix
```
**Lesson:** a silent default (`getattr(..., 500)`) hides a typo. Check what the exception class actually defines (`app/errors.py`).

### BUG-102: id type mismatch (str vs int)
`app/services/item_service.py`, `get_item`
Flask route params are strings (`"3"`), and the stored ids are ints (`3`), so `"3" == 3` is `False`.
```python
item_id = _parse_id(item_id)   # fix: add this line back (the helper already exists and delete_item uses it)
```
Another valid fix is the route converter `/<int:item_id>`. Then non-numeric ids return Flask's own 404, which is HTML, not JSON.

### BUG-103: Appending to a copy
`app/services/item_service.py`, `create_item`
`store.get_all()` returns `list(_items)`, which is a copy, so appending to it changes nothing in the store.
```python
store.get_all().append(item)   # bug
store.insert(item)             # fix
```
**Lesson:** read the docstring and implementation of the helper you're calling.

### BUG-104: Pagination off-by-one
`app/pagination.py`
```python
offset = page * limit          # bug: pages are 1-indexed
offset = (page - 1) * limit    # fix
```

### BUG-105: PATCH replaces instead of merging
`app/services/item_service.py`, `update_item`
```python
updated = {"id": existing["id"], **changes}                # bug: drops untouched fields
updated = {**existing, **changes, "id": existing["id"]}    # fix
```

### BUG-106: Missing "not found" check before deleting by index
`app/services/item_service.py`, `delete_item`
`next(..., -1)` returns `-1` when there's no match, and `list.pop(-1)` removes the **last** element.
```python
if index == -1:
    raise HttpError(404, f"Item {item_id} not found")   # fix: add back before remove_at
```

### BUG-107: Falsy check rejects 0
`app/validation.py`, `_check_quantity`
```python
if not quantity or not _is_int(quantity) or quantity < 0:   # bug: `not 0` is True
if not _is_int(quantity) or quantity < 0:                   # fix
```
**Lesson:** `if not x` treats `0`, `""`, `[]` and `None` the same. Use `is None` or a type check.

### BUG-108: Two bugs in stats
`app/services/item_service.py`, `get_stats`
```python
... // count     # bug: floor division gives 15.0
... / count      # fix: gives 15.9

item["quantity"] <= LOW_STOCK_THRESHOLD   # bug: "fewer than 10" means <
item["quantity"] <  LOW_STOCK_THRESHOLD   # fix
```
**Lesson:** one ticket, two causes. After the first fix, re-run the test and read the new diff.

### BUG-109: Frontend
`static/app.js`

1. **The Add form always errors.** The `fetch` POST doesn't send `Content-Type: application/json`. The route uses `request.get_json(silent=True) or {}`, so the body parses as `{}`, which fails with "name is required".
   ```js
   headers: { "Content-Type": "application/json" },   // fix: add back to the POST options
   ```
   *How to find it:* in DevTools Network, open the POST and check its request headers. The payload is there, but the content type is `text/plain`.

2. **Search does nothing.** The frontend sends `?q=...`, but the API reads `search`.
   ```js
   params.set("search", state.search);   // fix (was "q")
   ```
   *How to find it:* in the Network tab, compare the query string with the API table in the README. Contract mismatches between frontend and backend are very common in these rounds.

---

## Self-review questions (practice for "explain your fix")
- Why did fixing one line make 7 tests pass at once?
- For BUG-102, what are the trade-offs between `_parse_id` and `<int:item_id>`?
- What test would you add to catch BUG-109 automatically?
- Which of these bugs would a type checker or linter have caught?
