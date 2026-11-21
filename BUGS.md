# Bug List

Tick each box when its tests pass. Run `pytest -q` after every fix.

## Bugs

- [ ] **BUG-101: Bad requests crash the server.**
  A POST with no `name` returns **500**, and asking for an item that doesn't exist also returns **500**. These should be **400** and **404**.
  *Tests:* many

- [ ] **BUG-102: The item detail page is always "not found".**
  `GET /api/items/3` says item 3 doesn't exist, but item 3 (Stapler) is in the list.
  *Tests:* `TestGetItemById`

- [ ] **BUG-103: New items disappear.**
  `POST /api/items` returns 201, but the item never appears in the list and can't be fetched by id.
  *Tests:* `TestCreateItem`

- [ ] **BUG-104: The list is missing items.**
  The first page doesn't start with item 1, and page 2 shows what should be on page 3.
  *Tests:* `TestPagination`, `TestListItems`

- [ ] **BUG-105: Editing an item erases its details.**
  After changing only Gadget's price, its name, category and quantity are all gone.
  *Tests:* `TestUpdateItem`

- [ ] **BUG-106: Deleting a bad id deletes a real item.**
  `DELETE /api/items/999` returns 204, and the last item in the inventory disappears.
  *Tests:* `TestDeleteItem`

- [ ] **BUG-107: Can't add out-of-stock items.**
  Creating an item with `quantity: 0` is rejected, but 0 is valid.
  *Tests:* `TestValidation`

- [ ] **BUG-108: The stats panel numbers are wrong (2 causes).**
  The average price is too low, and "Notebook" (exactly 10 units) is flagged as low stock.
  *Tests:* `TestStats`

- [ ] **BUG-109: Frontend; check in the browser (2 causes).**
  The "Add item" form always shows an error with valid input, and the search box doesn't filter anything.
  *Tests:* none. Run `python run.py` and open http://localhost:5000

## Spec rules (what "correct" means)

- Errors are JSON `{"error": "..."}`. Invalid input returns **400**, a missing item returns **404**, and a client mistake should never get a **500**.
- `price` must be ≥ 0. `quantity` must be an integer ≥ 0, and **0 is valid**.
- Low stock means quantity **< 10**.
- `average_price` is the mean unit price, rounded to 2 decimals.
- Pages start at 1, so `page=1` is the first page. The default `limit` is 10.
- POST returns **201**. DELETE returns **204**. PATCH changes **only** the fields sent.

| Method | Path | Query / body |
|---|---|---|
| GET | `/api/items` | `page`, `limit`, `search`, `category` |
| GET | `/api/items/stats` | |
| GET | `/api/items/<id>` | |
| POST | `/api/items` | `name`, `price`, `quantity`, optional `category` |
| PATCH | `/api/items/<id>` | any of the above |
| DELETE | `/api/items/<id>` | |

## Commands

```powershell
.venv\Scripts\Activate.ps1
pytest -q --tb=line                 # quick summary of failures
pytest -v tests/test_items.py::TestStats   # one test class
pytest --lf                         # re-run only the last failures
python run.py                       # app at http://localhost:5000
```

## Done when

- [ ] `pytest` shows 20/20 passing
- [ ] In the browser you can add an item, search, page through the list, and delete
- [ ] You can explain each root cause in one sentence
