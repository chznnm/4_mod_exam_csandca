import requests
import pytest
from clients.api_manager import ApiManager
from data.auth.auth_data import ADMIN_CREDS
from utils.data_generator import DataGenerator

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="function")
def test_user():
    password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user, **kwargs):
    response = api_manager.auth_api.register_user(test_user, **kwargs).json()
    test_user["id"] = response["id"]
    return test_user

@pytest.fixture(scope="session")
def unauthenticated_api_manager(registered_user):
    session = requests.Session()
    yield ApiManager(session)
    session.close()

@pytest.fixture(scope="function")
def authenticated_user(api_manager,test_user):
    api_manager.auth_api.register_user(test_user)
    return api_manager.auth_api.authenticate((test_user["email"],test_user["password"]))

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
def authenticated_admin(api_manager):
    return api_manager.auth_api.authenticate((ADMIN_CREDS["email"],ADMIN_CREDS["password"]))

@pytest.fixture()
def create_new_movie(api_manager,test_movie,authenticated_admin):
    response = api_manager.movies_api.create_movie(test_movie)
    created_movie = response.json()
    yield created_movie
    try:
        api_manager.movies_api.delete_movie_by_id(created_movie["id"])
    except ValueError:
        pass

@pytest.fixture()
def test_review():
    return {
        "rating": DataGenerator.generate_random_rating(),
        "text": DataGenerator.generate_random_text_for_review()
    }

@pytest.fixture()
def create_new_review(api_manager,test_review,create_new_movie):
    created_movie_id = create_new_movie.get("id")
    return api_manager.movies_api.create_review_for_movie(created_movie_id,test_review).json()



@pytest.fixture()
def test_genre():
    return {
        "name":DataGenerator.generate_random_genre_name()
    }
@pytest.fixture()
def create_new_genre(api_manager,test_genre,authenticated_admin):
    response =  api_manager.movies_api.create_new_genre(test_genre).json()
    genre_id = response.get('id')
    yield response
    try:
        api_manager.movies_api.delete_genre_by_id(genre_id)
    except ValueError:
        pass


