"""
API conftest.py – fixtures and shared test data for all API tests.

Uses Playwright's APIRequestContext. Run API tests separately from UI tests
to avoid asyncio conflicts:
    python -m pytest api/tests/ -v
"""

import json
import pytest
from playwright.sync_api import Playwright, APIRequestContext
from api.client.pet_api_client import PetApiClient

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
MULTIPART_HEADERS = {"Accept": "application/json"}
BASE_URL = "https://petstore.swagger.io/v2"

# ── Shared API test data ──────────────────────────────────────────────────────
with open("test_data/api/api_test_data.json") as f:
    _TD = json.load(f)

PET_DATA = _TD["pet"]


# ── Session-scoped API request context ────────────────────────────────────────
@pytest.fixture(scope="session")
def api(playwright: Playwright) -> APIRequestContext:
    """Session-scoped Playwright API request context with JSON headers."""
    context = playwright.request.new_context(extra_http_headers=HEADERS)
    yield context
    context.dispose()


# ── Session-scoped PetApiClient ───────────────────────────────────────────────
@pytest.fixture(scope="session")
def pet_client(api: APIRequestContext) -> PetApiClient:
    """Session-scoped PetApiClient wrapping the API context."""
    return PetApiClient(api, BASE_URL)


# ── Session-scoped PetApiClient for multipart uploads ─────────────────────────
@pytest.fixture(scope="session")
def upload_pet_client(playwright: Playwright) -> PetApiClient:
    """PetApiClient using a context without Content-Type: application/json.
    Required for multipart/form-data endpoints like uploadImage."""
    context = playwright.request.new_context(extra_http_headers=MULTIPART_HEADERS)
    yield PetApiClient(context, BASE_URL)
    context.dispose()


# ── Module-scoped shared pet ──────────────────────────────────────────────────
@pytest.fixture(scope="module")
def created_pet(pet_client: PetApiClient) -> dict:
    """Create one pet for the module using data from api_test_data.json."""
    d = PET_DATA["default_pet"]
    payload = PetApiClient.build_payload(
        name=d["name"],
        status=d["status"],
        photo_urls=d["photo_urls"],
        pet_id=d["id"],
        category=d["category"],
        tags=d["tags"]
    )
    response = pet_client.create(payload)
    assert response.status == 200
    pet = response.json()
    yield pet
    pet_client.delete(pet["id"])
