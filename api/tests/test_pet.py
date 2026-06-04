"""
API Tests – Petstore Pet Endpoints (TC-PET-*)

Base URL : https://petstore.swagger.io/v2
Endpoint : /pet

Covers:
  TC-PET-01  POST /pet          – Create a new pet, verify 200 and returned id
  TC-PET-02  GET  /pet/{id}     – Retrieve the created pet by id
  TC-PET-03  PUT  /pet          – Update an existing pet's name and status
  TC-PET-04  GET  /pet/{id}     – Verify updated fields are persisted
  TC-PET-05  GET  /pet/findByStatus?status=available – All returned pets are available
  TC-PET-06  GET  /pet/findByStatus?status=pending   – All returned pets are pending
  TC-PET-07  GET  /pet/findByStatus?status=sold      – All returned pets are sold
  TC-PET-08  GET  /pet/findByStatus?status=invalid   – Returns 200 with empty list
  TC-PET-09  GET  /pet/{id}     – Returns 404 for non-existent pet
  TC-PET-10  DELETE /pet/{id}   – Delete a pet, verify subsequent GET returns 404
  TC-PET-11  POST /pet          – Body without photoUrls is accepted by design
  TC-PET-12  POST /pet          – Missing id field, server assigns its own id
  TC-PET-13  POST /pet          – String id returns 500
  TC-PET-14  POST /pet          – Malformed JSON with no id value returns 400
  TC-PET-15  POST /pet/{petId}/uploadImage – Upload image for a pet returns 200
"""

import pytest
from api.client.pet_api_client import PetApiClient
from api.conftest import PET_DATA


class TestPet:

    # ── TC-PET-01 ─────────────────────────────────────────────────────────────
    def test_create_pet_returns_200_and_id(self, pet_client: PetApiClient):
        """POST /pet – successful creation returns 200 and a non-zero id."""
        d = PET_DATA["create_pet"]
        payload = PetApiClient.build_payload(name=d["name"], status=d["status"],
                                             photo_urls=d["photo_urls"],
                                             pet_id=d["id"])
        response = pet_client.create(payload)

        assert response.status == 200
        body = response.json()
        assert body["id"] == d["id"]
        assert body["name"] == d["name"]
        assert body["status"] == d["status"]
        assert body["photoUrls"] == d["photo_urls"]

        pet_client.delete(body["id"])

    # ── TC-PET-02 ─────────────────────────────────────────────────────────────
    def test_get_pet_by_id(self, pet_client: PetApiClient, created_pet: dict):
        """GET /pet/{id} – returns a pet with the correct id."""
        response = pet_client.get(created_pet["id"])

        assert response.status == 200
        body = response.json()
        assert body["id"] == created_pet["id"]

    # ── TC-PET-03 ─────────────────────────────────────────────────────────────
    def test_update_pet(self, pet_client: PetApiClient, created_pet: dict):
        """PUT /pet – update name and status, returns 200 with updated fields."""
        payload = PetApiClient.build_payload(
            name=PET_DATA["updated_name"],
            status=PET_DATA["updated_status"],
            pet_id=created_pet["id"],
            photo_urls=created_pet.get("photoUrls", [])
        )
        response = pet_client.update(payload)

        assert response.status == 200
        body = response.json()
        assert body["name"] == PET_DATA["updated_name"]
        assert body["status"] == PET_DATA["updated_status"]

    # ── TC-PET-04 ─────────────────────────────────────────────────────────────
    def test_updated_fields_are_persisted(self, pet_client: PetApiClient, created_pet: dict):
        """PUT /pet then GET /pet/{id} – verify update is reflected.
        Re-applies update before reading back due to shared public server."""
        payload = PetApiClient.build_payload(
            name=PET_DATA["updated_name"],
            status=PET_DATA["updated_status"],
            pet_id=created_pet["id"],
            photo_urls=created_pet.get("photoUrls", [])
        )
        pet_client.update(payload)

        response = pet_client.get(created_pet["id"])
        assert response.status == 200
        body = response.json()
        assert body["name"] == PET_DATA["updated_name"]
        assert body["status"] == PET_DATA["updated_status"]

    # ── TC-PET-05/06/07 ───────────────────────────────────────────────────────
    @pytest.mark.parametrize("status", PET_DATA["valid_statuses"])
    def test_find_by_valid_status(self, pet_client: PetApiClient, status: str):
        response = pet_client.find_by_status(status)

        assert response.status == 200
        pets = response.json()
        assert isinstance(pets, list)
        assert all(p["status"] == status for p in pets)

    # ── TC-PET-08 ─────────────────────────────────────────────────────────────
    def test_find_by_invalid_status_returns_empty_list(self, pet_client: PetApiClient):
        response = pet_client.find_by_status(PET_DATA["invalid_status"])

        assert response.status == 200
        pets = response.json()
        assert isinstance(pets, list)
        assert len(pets) == 0

    # ── TC-PET-09 ─────────────────────────────────────────────────────────────
    def test_get_nonexistent_pet_returns_404(self, pet_client: PetApiClient):
        """GET /pet/{id} with a non-existent id – returns 404."""
        response = pet_client.get(PET_DATA["nonexistent_id"])
        assert response.status == 404

    # ── TC-PET-10 ─────────────────────────────────────────────────────────────
    def test_delete_pet(self, pet_client: PetApiClient):
        d = PET_DATA["delete_pet"]
        payload = PetApiClient.build_payload(name=d["name"], status=d["status"],
                                             photo_urls=d["photo_urls"])
        create_response = pet_client.create(payload)
        assert create_response.status == 200
        pet_id = create_response.json()["id"]

        delete_response = pet_client.delete(pet_id)
        assert delete_response.status == 200

        get_response = pet_client.get(pet_id)
        assert get_response.status == 404

    # ── TC-PET-11 ─────────────────────────────────────────────────────────────
    def test_create_pet_without_photo_urls_is_accepted(self, pet_client: PetApiClient):
        d = PET_DATA["no_photo_pet"]
        response = pet_client.create({"name": d["name"], "status": d["status"]})

        assert response.status == 200
        body = response.json()
        assert body["name"] == d["name"]

        pet_client.delete(body["id"])

    # ── TC-PET-12 ─────────────────────────────────────────────────────────────
    def test_create_pet_with_empty_id_assigns_server_id(self, pet_client: PetApiClient):
        """POST /pet with no id field – server assigns its own id and returns 200."""
        payload = {
            "name": PET_DATA["create_pet"]["name"],
            "status": PET_DATA["create_pet"]["status"],
            "photoUrls": PET_DATA["create_pet"]["photo_urls"]
        }
        response = pet_client.create(payload)

        assert response.status == PET_DATA["invalid_id_cases"]["empty_id_expected_status"]
        body = response.json()
        assert body["id"] > 0
        assert body["name"] == PET_DATA["create_pet"]["name"]

        pet_client.delete(body["id"])

    # ── TC-PET-13 ─────────────────────────────────────────────────────────────
    def test_create_pet_with_string_id_returns_500(self, pet_client: PetApiClient):
        """POST /pet with a string value for id – returns 500.
        The API expects id to be an integer; a string causes a server error."""
        payload = {
            "id": PET_DATA["invalid_id_cases"]["string_id"],
            "name": PET_DATA["create_pet"]["name"],
            "status": PET_DATA["create_pet"]["status"],
            "photoUrls": PET_DATA["create_pet"]["photo_urls"]
        }
        response = pet_client.create(payload)

        assert response.status == PET_DATA["invalid_id_cases"]["string_id_expected_status"]

    # ── TC-PET-14 ─────────────────────────────────────────────────────────────
    def test_create_pet_with_no_value_id_returns_400(self, pet_client: PetApiClient):
        """POST /pet with malformed JSON where id has no value e.g. "id": 
        This matches the curl behavior: {"id": ,"name":...} returns 500."""
        raw_payload = PET_DATA["invalid_id_cases"]["no_value_id_raw"]
        response = pet_client.create_raw(raw_payload)

        assert response.status == PET_DATA["invalid_id_cases"]["no_value_id_expected_status"]

    # ── TC-PET-15 ─────────────────────────────────────────────────────────────
    def test_upload_image_for_pet(self, upload_pet_client: PetApiClient, created_pet: dict):
        """POST /pet/{petId}/uploadImage – upload an image file for an existing pet."""
        d = PET_DATA["upload_image"]
        response = upload_pet_client.upload_image(
            pet_id=created_pet["id"],
            file_bytes=b"fake_image_bytes", # Mocking the binary data that server expects.
            filename=d["filename"],
            additional_metadata=d["additional_metadata"]
        )

        assert response.status == d["expected_status"]
        body = response.json()
        assert body["code"] == 200
        assert d["filename"] in body["message"]
        assert d["additional_metadata"] in body["message"]

