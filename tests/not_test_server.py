import sys

from fastapi.testclient import TestClient

sys.path.append("./app")
from main import app


client = TestClient(app)


def test_liveness():
    response = client.get("/probe/liveness")
    assert response.status_code == 200


def test_create_success():
    response = client.get("/v1/word?q=nice&source_code=en&target_code=de")
    assert response.status_code == 201


def test_create_404():
    response = client.get("/v1/word?q=ncer2&source_code=en&target_code=de")
    assert response.status_code == 404


def test_create_400():
    response = client.get("/v1/word?q=ncer2&source_code=en&target_code=den")
    assert response.status_code == 400


def test_delete_success():
    client.get("/v1/word?q=nice&source_code=en&target_code=de")
    response = client.delete("/v1/word?q=nice&source_code=en&target_code=de")
    assert response.status_code == 200
    assert response.json() == {'deleted count':  1}


def test_delete_404():
    response = client.delete("/v1/word?q=nice&source_code=en&target_code=de")
    assert response.status_code == 404


def test_words_list_basic():
    client.get("/v1/word?q=nice&source_code=en&target_code=de")
    response = client.get("/v1/words?q=nice")
    assert response.status_code == 200
    test_data = response.json()
    assert len(test_data) == 1
    assert test_data[0].get("definitions", None) is None
    assert test_data[0].get("translations", None) is None


def test_words_list_full():
    client.get("/v1/word?q=nice&source_code=en&target_code=de")
    response = client.get("/v1/words?q=nice&include_definitions=true&include_translations=true")
    assert response.status_code == 200
    test_data = response.json()
    assert len(test_data) == 1
    assert test_data[0].get("definitions", None) is not None
    assert test_data[0].get("translations", None) is not None


def test_words_list_2():
    client.get("/v1/word?q=nice&source_code=en&target_code=de")
    client.get("/v1/word?q=Nirwana&source_code=de&target_code=en")
    response = client.get("/v1/words?q=ni")
    assert response.status_code == 200
    test_data = response.json()
    assert len(test_data) == 2