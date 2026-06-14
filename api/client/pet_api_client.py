"""
PetApiClient – encapsulates all HTTP interactions with the /pet endpoint.

Uses Playwright's APIRequestContext — the same library used for UI automation,
keeping the stack consistent.

Run API tests separately to avoid asyncio conflicts with UI tests:
    python -m pytest api/tests/ -v   (API only)
    python -m pytest ui/tests/ -v    (UI only)

Mirrors the Page Object pattern used in the UI layer:
  - Locators       → endpoint URLs
  - Page actions   → HTTP methods (create, get, update, delete, find_by_status)
"""

from playwright.sync_api import APIRequestContext, APIResponse


class PetApiClient:

    def __init__(self, api: APIRequestContext, base_url: str):
        self.api = api
        self.base_url = base_url

    # ── URL builder ───────────────────────────────────────────────────────────

    def _url(self, path: str) -> str:
        """Build full URL from relative path using base_url from conftest."""
        return f"{self.base_url}{path}"

    # ── CRUD methods ──────────────────────────────────────────────────────────

    def create(self, payload: dict) -> APIResponse:
        """POST /pet – create a new pet."""
        return self.api.post(self._url("/pet"), data=payload)

    def create_raw(self, raw_body: str) -> APIResponse:
        """POST /pet with a raw JSON string body – used for malformed payload testing."""
        return self.api.post(
            self._url("/pet"),
            data=raw_body,
            fail_on_status_code=False
        )

    def get(self, pet_id: int) -> APIResponse:
        """GET /pet/{id} – retrieve a pet by id."""
        return self.api.get(
            self._url(f"/pet/{pet_id}"),
            fail_on_status_code=False
        )

    def update(self, payload: dict) -> APIResponse:
        """PUT /pet – update an existing pet."""
        return self.api.put(self._url("/pet"), data=payload)

    def delete(self, pet_id: int) -> APIResponse:
        """DELETE /pet/{id} – delete a pet."""
        return self.api.delete(
            self._url(f"/pet/{pet_id}"),
            fail_on_status_code=False
        )

    def find_by_status(self, status: str) -> APIResponse:
        """GET /pet/findByStatus – filter pets by status."""
        return self.api.get(
            self._url("/pet/findByStatus"),
            params={"status": status},
            fail_on_status_code=False
        )

    def upload_image(self, pet_id: int, file_bytes: bytes,
                     filename: str = "test.jpg",
                     additional_metadata: str | None = None) -> APIResponse:
        """POST /pet/{petId}/uploadImage – upload an image for a pet."""
        multipart: dict = {
            "file": {"name": filename, "mimeType": "image/jpeg", "buffer": file_bytes}
        }
        if additional_metadata is not None:
            multipart["additionalMetadata"] = additional_metadata
        return self.api.post(
            self._url(f"/pet/{pet_id}/uploadImage"),
            multipart=multipart,
            fail_on_status_code=False
        )

    # ── Payload factory ───────────────────────────────────────────────────────

    @staticmethod
    def build_payload(
        name: str,
        status: str,
        photo_urls: list[str],
        pet_id: int = 0,
        category: dict | None = None,
        tags: list[dict] | None = None,
    ) -> dict:
        """Build a pet payload dict from explicit values."""
        payload = {
            "id": pet_id,
            "name": name,
            "status": status,
            "photoUrls": photo_urls,
        }
        if category is not None:
            payload["category"] = category
        if tags is not None:
            payload["tags"] = tags
        return payload
