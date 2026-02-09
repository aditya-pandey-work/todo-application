def test_create_and_get_todo(client):
    client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword",
        },
    )
    
    login = client.post(
        "/login",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/todos/create",
        json={"title": "My first todo"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "My first todo"

    response = client.get(
        "/api/todos/get",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
