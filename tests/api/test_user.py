
from models.base_models import RegisterUserResponse


class TestUserSuccessful:

    #Созданиие пользователя
    def test_create_user(self, super_admin, creation_user_data):

        response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = RegisterUserResponse(**response.json())

        assert created_user.email == creation_user_data.email
        assert created_user.fullName == creation_user_data.fullName
        assert created_user.roles == creation_user_data.roles
        assert created_user.verified is True

    #Получение пользователя по id или email
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        #Создаем пользователя и валидируем его
        created_user_response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = RegisterUserResponse(**created_user_response.json())

        #Вызываем метод гет по айди и валидируем его
        response_by_id = super_admin.api.user_api.get_user_info(created_user.id)
        response_by_id_model = RegisterUserResponse(**response_by_id.json())

        # Вызываем метод гет по емейл и валидируем его
        response_by_email = super_admin.api.user_api.get_user_info(creation_user_data.email)
        response_by_email_model = RegisterUserResponse(**response_by_email.json())

        #Проверки
        assert response_by_id_model == response_by_email_model, "Содержание ответов должно быть идентичным"
        assert response_by_id_model.id and response_by_email_model.id != '', "ID должен быть не пустым"
        assert response_by_id_model.email == creation_user_data.email
        assert response_by_id_model.fullName == creation_user_data.fullName
        assert response_by_id_model.roles == creation_user_data.roles
        assert response_by_id_model.verified is True


class TestUserNegative:

    #Получение пользователя по id с ролью USER
    def test_get_user_by_id_common_user(self, common_user):

        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

        #Проверки корректности ошибки