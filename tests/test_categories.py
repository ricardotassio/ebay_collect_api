from http import HTTPStatus

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_get_categories():
    response = client.get('/api/categories')
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), dict)
    assert 'holiday_decor' in response.json()
