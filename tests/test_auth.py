
def test_register(client):
    response = client.post(
        "/register", 
        json = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Registered"

def test_login(client):
    client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )
    response = client.post(
        "/login", 
        json = {
            "email": "test@example.com", 
            "password": "testpassword"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
