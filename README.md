# Inventory Tracker — Mock Debugging Assessment

A small full-stack app: a **Flask REST API** (`app/`) and a **vanilla JS frontend** (`static/`).
Several bugs have been reported. Your job is to find and fix them.

**Time limit:** 90 minutes. Start a timer.
**Rules:** don't open `.answer-key/` until you're done. You may use an AI assistant, but treat it the way the real round does: ask narrow questions and verify every answer.

---

## Setup

```bash
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# macOS/Linux:           source .venv/bin/activate
pip install -r requirements.txt

pytest -v            # run the test suite
python run.py        # start the app at http://localhost:5000
```

## API

| Method | Path                | Description                                                  |
|--------|---------------------|--------------------------------------------------------------|
| GET    | `/api/items`        | List items. Query: `page` (1-based), `limit`, `search`, `category` |
| GET    | `/api/items/stats`  | Inventory summary                                            |
| GET    | `/api/items/<id>`   | Get one item                                                 |
| POST   | `/api/items`        | Create an item (`name`, `price`, `quantity`, optional `category`) → `201` |
| PATCH  | `/api/items/<id>`   | Partially update an item                                     |
| DELETE | `/api/items/<id>`   | Delete an item → `204`                                       |

**Error contract:** every error response is JSON `{"error": "<message>"}`.
Use `400` for invalid input and `404` for a missing item. A `500` should never be returned for a client mistake.

**Business rules:**
- `price` is a non-negative number. `quantity` is a non-negative integer (out-of-stock items have quantity `0`).
- An item is **low stock** when it has **fewer than 10** units.
- `average_price` in stats is the mean unit price across all items, rounded to 2 decimals.

---

## Bug reports

> These were written by users and QA, not engineers. They describe symptoms, not causes.
> One root cause can produce several symptoms, and one ticket can have more than one cause.

**BUG-101: Bad requests crash the server.**
QA sent a POST with no `name` and got `500 Internal Server Error`. Asking for an item that doesn't exist also gives a 500. Per the error contract, these should be 400 and 404.

**BUG-102: The item detail page is always "not found".**
`GET /api/items/3` says item 3 doesn't exist, but item 3 (Stapler) is clearly in the list.

**BUG-103: New items disappear.**
`POST /api/items` returns 201 with the new item, but the item never shows up in the list afterwards and can't be fetched by id.

**BUG-104: The list is missing items.**
The first page of the item list doesn't start with item 1. Users also say page 2 shows what should be on page 3.

**BUG-105: Editing an item erases its details.**
A user changed only the price of "Gadget". Afterwards it had no name, category, or quantity.

**BUG-106: Deleting a bad id deletes a real item.**
`DELETE /api/items/999` (which doesn't exist) returned 204, and the last item in the inventory vanished.

**BUG-107: Can't add out-of-stock items.**
Creating an item with `quantity: 0` is rejected, even though 0 is a valid quantity.

**BUG-108: The stats panel numbers are wrong.**
Finance says the average price shown is too low. Also, "Notebook" is flagged as low stock even though it has exactly 10 units.

**BUG-109 (frontend; check manually in the browser): The Add form and search are broken.**
- Submitting the "Add item" form with valid values always shows an error.
- Typing in the search box doesn't filter the table.

*No automated tests cover BUG-109. Use the browser DevTools Network tab.*

---

## Done when

- `pytest` is all green (20 tests).
- In the browser, you can add an item, search the list, page through it, and delete an item.
- You can explain the root cause of every fix in one sentence.

When you're done, compare your fixes with `.answer-key/SOLUTIONS.md`. `.answer-key/reference/` has the fully working code.
