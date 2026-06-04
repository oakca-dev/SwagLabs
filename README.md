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

Run a specific file:

```bash
python -m pytest ui/tests/test_auth.py -v
python -m pytest ui/tests/test_cart.py -v
python -m pytest ui/tests/test_checkout.py -v
python -m pytest ui/tests/test_inventory.py -v
```

Run in headed mode (see the browser):

```bash
python -m pytest ui/tests/ -v --headed
```

### Run API tests

```bash
python -m pytest api/tests/ -v
```

---

## What is Covered

### UI — Swag Labs (`ui/tests/`)

| Area | Tests | File |
|---|---|---|
| Authentication | TC-AUTH-01 to TC-AUTH-07 (10 runs via parametrize) | `test_auth.py` |
| Inventory | TC-INV-01 to TC-INV-07 | `test_inventory.py` |
| Shopping Cart | TC-CART-01 to TC-CART-07 | `test_cart.py` |
| Checkout | TC-CHK-01 to TC-CHK-08 | `test_checkout.py` |

See **flows.txt** for full scenario descriptions and design decisions.

### API — Petstore (`api/tests/`)

| Endpoint | Tests |
|---|---|
| `POST /pet` | TC-PET-01, 11, 12, 13, 14 |
| `GET /pet/{id}` | TC-PET-02, 04, 09 |
| `PUT /pet` | TC-PET-03 |
| `DELETE /pet/{id}` | TC-PET-10 |
| `GET /pet/findByStatus` | TC-PET-05, 06, 07, 08 |
| `POST /pet/{petId}/uploadImage` | TC-PET-15 |

See **api-tests.txt** for full scenario descriptions and design decisions.
