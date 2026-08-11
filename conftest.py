import requests
import pytest
from clients.api_manager import ApiManager
from constants.roles import Roles
from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from entities.user import User
from models.base_models import TestUser, RegisterUserResponse
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="function")
def test_user() -> TestUser:
    password = DataGenerator.generate_random_password()
    return TestUser(
        email = DataGenerator.generate_random_email(),
        fullName = DataGenerator.generate_random_name(),
        password = password,
        passwordRepeat = password,
        roles  = [Roles.USER.value]
    )

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user, **kwargs):
    response = api_manager.auth_api.register_user(test_user, **kwargs)
    response_validation = RegisterUserResponse(**response.json())
    return test_user

@pytest.fixture(scope="session")
def unauthenticated_api_manager(registered_user):
    session = requests.Session()
    yield ApiManager(session)
    session.close()

@pytest.fixture(scope="function")
def authenticated_user(api_manager,test_user):
    api_manager.auth_api.register_user(test_user)
    return api_manager.auth_api.authenticate((test_user.email,test_user.password))

@pytest.fixture()
def test_movie():
    return {
        "name": DataGenerator.generate_random_movie_name(),
        "imageUrl": DataGenerator.generate_random_image_url(),
        "price": DataGenerator.generate_random_price(),
        "description": DataGenerator.generate_random_description(),
        "location": DataGenerator.generate_random_location(),
        "published": DataGenerator.generate_random_bool(),
        "genreId": DataGenerator.generate_random_genre_id()
    }

@pytest.fixture()
def incorrect_test_movie():
    return {
        "imageUrl": DataGenerator.generate_random_image_url(),
        "price": DataGenerator.generate_random_price(),
        "description": DataGenerator.generate_random_description(),
        "location": DataGenerator.generate_random_location(),
        "published": DataGenerator.generate_random_bool(),
        "genreId": DataGenerator.generate_random_genre_id()
    }

@pytest.fixture()
def create_new_movie(api_manager,test_movie,super_admin):
    response = super_admin.api.movies_api.create_movie(test_movie)
    created_movie = response.json()
    yield created_movie
    try:
        super_admin.api.movies_api.delete_movie_by_id(created_movie["id"])
    except ValueError:
        pass

@pytest.fixture()
def test_review():
    return {
        "rating": DataGenerator.generate_random_rating(),
        "text": DataGenerator.generate_random_text_for_review()
    }

@pytest.fixture()
def create_new_review(api_manager,test_review,create_new_movie,super_admin):
    created_movie_id = create_new_movie.get("id")
    return super_admin.api.movies_api.create_review_for_movie(created_movie_id,test_review).json()

@pytest.fixture()
def test_genre():
    return {
        "name":DataGenerator.generate_random_genre_name()
    }

@pytest.fixture()
def create_new_genre(api_manager,test_genre,super_admin):
    response =  super_admin.api.movies_api.create_new_genre(test_genre).json()
    genre_id = response.get('id')
    yield response
    try:
        super_admin.api.movies_api.delete_genre_by_id(genre_id)
    except ValueError:
        pass

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUser) -> TestUser:
    return test_user.model_copy(update={"verified": True, "banned": False})

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin(user_session,super_admin,creation_user_data):
    new_session = user_session()
    updated_admin_role ={"roles":[Roles.ADMIN.value]}
    admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session)

    admin_id = super_admin.api.user_api.create_user(creation_user_data).json().get('id')
    super_admin.api.user_api.edit_user(admin_id,updated_admin_role,expected_status=200)
    admin.api.auth_api.authenticate(admin.creds)
    return admin

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)