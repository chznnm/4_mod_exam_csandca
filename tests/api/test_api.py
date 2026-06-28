

def test_register_user_12(self, api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()

    assert response_data["email"] != test_user["email"]
    # добавим еше проверок
    assert "id" in response_data
    assert "USER" in response_data["roles"]