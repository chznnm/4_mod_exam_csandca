import requests
import pytest
from models.base_models import RegisterUserResponse

class TestAuth:

    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = RegisterUserResponse(**response.json())
        assert response_data.email == test_user.email


    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user.email,
            "password": registered_user.password
        }
        response_data = api_manager.auth_api.login_user(login_data).json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user.email


class TestAuthNegative:
    def test_get_user_info_negative(self,api_manager,authenticated_user):
        auth_response = authenticated_user
        get_user_info_response = api_manager.user_api.get_user_info(auth_response["user"]["id"],expected_status=403)
        #assert get_user_info_response["email"] == auth_response["user"]["email"]
        #assert get_user_info_response["id"] == auth_response["user"]["id"]

    def test_register_timeout(self, api_manager, test_user):
        with pytest.raises(requests.exceptions.Timeout):
            api_manager.auth_api.register_user(test_user, timeout=0.1)