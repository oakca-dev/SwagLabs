# SwagLabs Automation Project

Automated test suite for [Swag Labs](https://www.saucedemo.com) (UI) and [Petstore API](https://petstore.swagger.io).

---

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 | Language |
| Playwright for Python | 1.60 | Browser automation (UI) and API requests (API) |
| pytest | 9.0 | Test runner, fixtures, parametrize |

---

## Project Structure

```
SwagLabs/
├── ui/
│   ├── conftest.py          # Browser/page fixtures and shared test data
│   ├── pages/               # Page Object Models (one file per page)
│   └── tests/               # UI test files
├── api/
│   ├── conftest.py          # API request context fixtures
│   ├── client/
│   │   └── pet_api_client.py  # PetApiClient (HTTP methods + payload builder)
│   └── tests/               # API test files
├── test_data/
│   ├── ui/ui_test_data.json   # Users, products, error messages, checkout data
│   └── api/api_test_data.json # Pet payloads, statuses, edge case inputs
├── flows.txt                # UI test scenarios and design decisions
├── api-tests.txt            # API test scenarios and design decisions
└── pytest.ini               # pytest config (defaults to ui/tests)
```

---

## Important

**UI and API tests must be run in separate pytest sessions.**

Playwright's sync API cannot run inside the asyncio event loop started by
`pytest-playwright` when both test types run together.

---

## Running the Tests

### Install dependencies (first time only)

```bash
pip install pytest playwright pytest-playwright
playwright install chromium
```

### Run UI tests

```bash
python -m pytest ui/tests/ -v
```

Run in headed mode (see the browser):

```bash
python -m pytest ui/tests/ -v --headed
```

Run on Firefox:

```bash
python -m pytest ui/tests/ -v --browser firefox
```

Run on Safari (WebKit):

```bash
python -m pytest ui/tests/ -v --browser webkit
```

Run a specific file:

```bash
python -m pytest ui/tests/test_auth.py -v
python -m pytest ui/tests/test_cart.py -v
python -m pytest ui/tests/test_checkout.py -v
python -m pytest ui/tests/test_inventory.py -v
```

### Run API tests

```bash
python -m pytest api/tests/ -v
```

---

## What is Covered

### UI — Swag Labs (`ui/tests/`) — 33 test runs

| File | Tests | Scenarios |
|---|---|---|
| `test_auth.py` | 13 runs | Login success (x4 users), login errors (locked, wrong pass, blank user, blank pass, both empty, long username, special chars), logout, unauthenticated redirect |
| `test_inventory.py` | 7 | Product count, sort A-Z/Z-A/price asc/desc, product detail open, detail elements |
| `test_cart.py` | 7 | Add single/multiple items, remove from inventory/cart, persistence, empty cart |
| `test_checkout.py` | 9 | Happy path, empty cart, 3 validation errors, subtotal (1 item), subtotal (2 items), cancel, cart empty after order |

See **flows.txt** for full scenario descriptions and design decisions.

### API — Petstore (`api/tests/`) — 23 test runs

| Endpoint | Tests | Scenarios |
|---|---|---|
| `POST /pet` | 13 | Create, no photoUrls, empty/string/null/negative/large id, long/special/unicode name, null name, invalid content-type, malformed JSON |
| `GET /pet/{id}` | 2 | Retrieve by id, non-existent id (404) |
| `PUT /pet` | 1 | Update name+status, verify persistence via GET |
| `DELETE /pet/{id}` | 1 | Delete, verify subsequent GET returns 404 |
| `GET /pet/findByStatus` | 4 | available, pending, sold (parametrized), invalid status (empty list) |
| `POST /pet/{petId}/uploadImage` | 2 | With file (200), without file (500) |

See **api-tests.txt** for full scenario descriptions and design decisions.
