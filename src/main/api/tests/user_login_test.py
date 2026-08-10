import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.login_user_request import LoginUserRequest

@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username="admin", password="123456")

        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username, f"Ошибка! Username админа в ответе API ({response.user.username}) не совпадает с запрошенным ({login_user_request.username})"
        assert response.user.role == "ROLE_ADMIN", f"Ошибка! Роль в ответе API ({response.user.role}) отличается от ожидаемой (ROLE_ADMIN)"


    def test_login_user(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, f"Ошибка! Username пользователя в ответе API ({response.user.username}) не совпадает с запрошенным ({create_user_request.username})"
        assert response.user.role == "ROLE_USER", f"Ошибка! Роль в ответе API ({response.user.role}) отличается от ожидаемой (ROLE_USER)"


    def test_login_user_invalid_password(self, api_manager: ApiManager, create_user_request):

        invalid_login_request = LoginUserRequest(username=create_user_request.username, password="WRONG_PASSWORD")

        api_manager.admin_steps.login_user_invalid_password(invalid_login_request)