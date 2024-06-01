from fastapi.testclient import TestClient
import pytest
import responses

from httpx import Response
from pytest_httpx import HTTPXMock

from .main import app

client = TestClient(app)


def test_read_item():
    # Include the required 'token' query parameter in the request URL
    response = client.get("/wibble/foo?token=wibble", headers={"X-Token": "coneofsilence"})

    # Print the response status code
    print("Response Status Code:", response.status_code)

    # Print the response JSON data
    print("Response JSON:", response.json())

    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_httpx(mocker):
    mock_response = {
        "mock_key": "mock_value"
    }

    mocker.patch(
        "httpx.get",
        side_effect=lambda url, *args, **kwargs: Response(
            200, json=mock_response
        ) if url == 'https://api.github.com/events' else Response(404)
    )
    response = client.get("/http?token=wibble", headers={"X-Token": "coneofsilence"})

    # Print the response status code
    print("Response Status Code:", response.status_code)

    # Print the response JSON data
    print("Response JSON:", response.json())

    assert response.status_code == 200
    assert response.json() == {
        "mock_key": "mock_value"
    }


def test_httpx_httpxmock(httpx_mock):
    expected_url = 'https://api.github.com/events'
    mock_response = {
        "mock_key": "mock_value"
    }

    httpx_mock.add_response(method="GET", url=expected_url, json=mock_response)

    response = client.get("/http?token=wibble", headers={"X-Token": "coneofsilence"})

    # Print the response status code
    print("Response Status Code:", response.status_code)

    # Print the response JSON data
    print("Response JSON:", response.json())

    assert response.status_code == 200
    assert response.json() == {
        "mock_key": "mock_value"
    }
