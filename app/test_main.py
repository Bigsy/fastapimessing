from fastapi.testclient import TestClient

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


