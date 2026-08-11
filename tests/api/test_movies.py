import allure
import pytest

from  tests.helpers.assertions import assert_movie_data_matches,assert_review_data_matches
from data.movie.movie_data import generate_edited_movie_data, generate_edited_review_data
from models.base_models import MoviesModel,ReviewModel,GetMoviesResponseModel

class TestMoviesSuccessful:


    @allure.epic("Movies api")
    @allure.story("Positive")
    @allure.description("Этот тест проверяет корректность метода, который возвращает все фильмы.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Получение всех фильмов без фильтров")
    @pytest.mark.smoke
    def test_get_movies(self,api_manager):
        with allure.step("Вызываем метод GET /movies"):
            response = api_manager.movies_api.get_movies().json()
        with allure.step("Проверяем, что ответ соответствует схеме"):
            GetMoviesResponseModel(**response)
        with allure.step("Проверяем, что массив movies не пустой."):
            assert response.get('movies') is not  None

    @allure.epic("Movies api")
    @allure.story("Positive")
    @allure.description("Этот тест проверяет корректность метода, который возвращает фильмы с фильтрами,но только одну страницу.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Получение фильмов без фильтров")
    def test_get_movies_with_params(self,api_manager):
        with allure.step("Вызываем метод GET /movies с параметром locations:MSK"):
            response = api_manager.movies_api.get_movies(params={'locations':'MSK'}).json()
        with allure.step("Проходим циклом по полученному массиву, и проверяем что у всех фильмов locations:MSK"):
            for movie in response['movies']:
                assert movie['location'] == 'MSK',f'expected: MSK, received:{movie['location']}'

    @allure.epic("Movies api")
    @allure.story("Positive")
    @allure.description("""Этот тест проверяет корректность создания фильма. Шаги:
    1. Создание фильма.
    2. Проверка полученных данных в ответе.
    3. Проверка корректности данных в БД.
    4. Проверка успешного получения фильма методом GET /movies{id}.""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание фильма")
    @pytest.mark.flaky(reruns=3)
    @pytest.mark.smoke
    def test_create_new_movie(self,api_manager, test_movie,create_new_movie,db_helper):
        with allure.step("Создаем новый фильм"):
            response = create_new_movie
        with allure.step("Проверяем, что ответ соответствует схеме"):
            MoviesModel(**response)
        with allure.step("Проверяем, что данные фильма из ответа соответствуют отправленным на сервер "):
            assert_movie_data_matches(test_movie, response)
        with allure.step("Ищем созданный фильм в БД"):
            response_from_db = db_helper.get_movie_by_id_from_db(response['id'])
        with allure.step("Проверяем, что данные в бд корректны"):
            assert response_from_db.id == response['id']
            assert response_from_db.name == response['name']
            assert response_from_db.price == response['price']
        with allure.step("Вызовем метод GET /Movies{id}"):
            get_response = api_manager.movies_api.get_movie_by_id(response.get("id"))
        with allure.step("Проверяем, что ответ соответствует схеме"):
            MoviesModel(**get_response.json())
        with allure.step("Проверим, что полученный фильм соответствует  созданному"):
            assert_movie_data_matches(test_movie,get_response.json())

    @allure.epic("Movies api")
    @allure.story("Positive")
    @allure.description("Этот тест проверяет корректность метода, который возвращает фильм по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Получение фильма по ID")
    @pytest.mark.smoke
    @pytest.mark.flaky(reruns=3)
    def test_get_movie_by_id(self,api_manager,create_new_movie,test_movie):
        with allure.step("Создаем фильм"):
            created_movie_id = create_new_movie.get('id')
        with allure.step("Вызываем метод GET /Movies{id} "):
            get_movie_by_id_response =  api_manager.movies_api.get_movie_by_id(movie_id=created_movie_id).json()
        with allure.step("Проверяем, что ответ соответствует схеме"):
            MoviesModel(**get_movie_by_id_response)
        with allure.step("Проверяем что данные созданного фильма соответствуют полученным"):
            assert_movie_data_matches(test_movie,get_movie_by_id_response)

    @allure.epic("Movies api")
    @allure.story("Positive")
    @allure.description("Этот тест проверяет корректность метода, который удаляет фильм по ID, а так же ролевую модель на этом методе")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление фильма по ID с ролевой моделью")
    @pytest.mark.flaky(reruns=3)
    @pytest.mark.regression
    @pytest.mark.parametrize("role,status_code",[
        ("super_admin",200),
        ("admin",403),
        ("common_user",403)
    ])
    def  test_delete_movie_by_id(self,request,super_admin,create_new_movie, test_movie,role,status_code,db_helper):
        with allure.step("Создаем фильм"):
            created_movie_id = create_new_movie.get("id")
        with allure.step("Определяем роль"):
            if role == "super_admin":
                current_user = super_admin
            else:
                current_user = request.getfixturevalue(role)
        with allure.step("Вызываем метод DELETE /movies{id}"):
            delete_movie_response = current_user.api.movies_api.delete_movie_by_id(created_movie_id,expected_status=status_code).json()

        if status_code == 200:
            with allure.step("В случае успешного удаления:"):
                with allure.step("Проверяем, что ответ соответствует схеме"):
                    MoviesModel(**delete_movie_response)
                with allure.step("Проверяем, что данные созданного фильма и  удаленного соответствуют"):
                    assert_movie_data_matches(test_movie,delete_movie_response)
                with allure.step("Проверяем методом GET /movies{id}, что фильм удален"):
                    current_user.api.movies_api.get_movie_by_id(created_movie_id,expected_status=404)
                with allure.step("Отправляем SELECT запрос в БД с id удаленного фильма"):
                    db_response = db_helper.get_movie_by_id_from_db(created_movie_id)
                with allure.step("Проверяем, что фильм не найден в БД"):
                    assert db_response is None
        else:
            with allure.step("В случае, если прав нет:"):
                with allure.step("Отправляем запрос GET /movies{id}"):
                    get_movie_by_id_response = current_user.api.movies_api.get_movie_by_id(created_movie_id,expected_status=200).json()
                with  allure.step("Проверяем, что фильм  не удален и данные соответствуют тем, которые переданы при создании"):
                    assert_movie_data_matches(test_movie,get_movie_by_id_response)

    @allure.epic("Movies api")
    @allure.story("Positive")
    @allure.description("Этот тест проверяет корректность метода, который редактирует фильм по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Редактирование фильма по ID ")
    @pytest.mark.flaky(reruns=3)
    @pytest.mark.smoke
    def test_edit_created_movie_by_id(self,super_admin,create_new_movie,test_movie):
        with allure.step("Создаем фильм"):
            created_movie_id = create_new_movie.get("id")
        with allure.step("Отправляем запрос PATCH /movies/{id}"):
            edited_movie_response = super_admin.api.movies_api.edit_movie_by_id(created_movie_id,generate_edited_movie_data()).json()
        with allure.step("Проверяем, что ответ соответствует схеме"):
            MoviesModel(**edited_movie_response)
        with allure.step("Отправляем GET /movies/{id}"):
            get_response = super_admin.api.movies_api.get_movie_by_id(created_movie_id).json()
        with allure.step("Проверяем, что ответ соответствует схеме."):
            MoviesModel(**get_response)
        with allure.step("Проверяем, что измененния применились"):
            assert edited_movie_response["name"] == get_response["name"],f'Expected:{edited_movie_response['name']}, Received:{get_response['name']}'
            assert edited_movie_response["price"] == get_response["price"],f'Expected:{edited_movie_response['price']}, Received:{get_response['price']}'
            assert test_movie["imageUrl"] == get_response["imageUrl"],f'Expected:{edited_movie_response['imageUrl']}, Received:{get_response['imageUrl']}'
            assert test_movie["description"] == get_response["description"],f'Expected:{edited_movie_response['description']}, Received:{get_response['description']}'
            assert test_movie["location"] == get_response["location"],f'Expected:{edited_movie_response['location']}, Received:{get_response['location']}'
            assert test_movie["published"] == get_response["published"],f'Expected:{edited_movie_response['published']}, Received:{get_response['published']}'

    @allure.epic("Movies api")
    @allure.story("Positive")
    @allure.description("Этот тест проверяет корректность работы фильтров метода GET /movies ")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title(""""Проверка фильтров GET /movies c параметрами:
                  minPrice = {min_price},
                  maxPrice = {max_price},
                  locations = {locations},
                  genreId = {genre_id} """)
    @pytest.mark.parametrize("min_price,max_price,locations,genre_id",[
        (1,500,["MSK"],4),
        (501,1000,["SPB"],5),
        (1,1000,['MSK','SPB'],4)
    ])
    @pytest.mark.regression
    def test_get_all_movies_with_parametrize(self,super_admin,min_price,max_price,locations,genre_id):
        params = {
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": locations,
            "genreId": genre_id
        }
        with allure.step("""Вызываем метод GET/ movies c параметрами 
                  minPrice = {min_price},
                  maxPrice = {max_price},
                  locations = {locations},
                  genreId = {genre_id}"""):
            response = super_admin.api.movies_api.get_movies(expected_status=200,params = params).json()
        with allure.step("Проверяем, что есть фильмы удовлетворяющие условиям"):
            assert response['movies'],"No movies found"
        with allure.step("Проверяем, что ответ соответствует схеме"):
            GetMoviesResponseModel(**response)
        with allure.step("Проверяем, что все фильмы соответствуют указанным в условии фильтрам"):
            for movie in response['movies']:
                assert movie['location'] in locations
                assert min_price <= movie['price'] <= max_price
                assert movie['genreId'] == genre_id

class TestReviewsSuccessful:

    #Получение отзывов фильма по ID
    def test_get_all_reviews(self,api_manager,create_new_movie):
        created_movie_id = create_new_movie.get('id')
        api_manager.movies_api.get_reviews_by_movie_id(created_movie_id)

    #Создание отзыва к фильму
    def test_create_review(self,create_new_review,test_review):
        response = create_new_review
        assert_review_data_matches(test_review,response)

    #Редактирование отзыва к фильму
    def test_edit_review(self,super_admin,create_new_review,create_new_movie):
        created_movie_id = create_new_movie.get('id')
        edited_review_data = generate_edited_review_data()
        edited_review_response = super_admin.api.movies_api.edit_review_by_movie_id(created_movie_id,edited_review_data).json()
        assert_review_data_matches(edited_review_data,edited_review_response)
        get_review_response = super_admin.api.movies_api.get_reviews_by_movie_id(created_movie_id).json()
        user_id = create_new_review.get('userId')
        found_review = None
        for review in get_review_response:
            if review.get('userId') == user_id:
                found_review = review
                break
        assert_review_data_matches(edited_review_data,found_review)

    #Удаление отзыва к фильму
    def test_delete_review(self,super_admin,create_new_review, create_new_movie):
        created_movie_id = create_new_movie.get('id')
        user_id = create_new_review.get('userId')
        super_admin.api.movies_api.delete_review_by_movie_id(created_movie_id,user_id)
        get_review_response = super_admin.api.movies_api.get_reviews_by_movie_id(created_movie_id).json()
        found_review = None
        for review in get_review_response:
            if review.get('userId') == user_id:
                found_review = review
                break
        assert found_review is None, f'Expected: None, received: {found_review}'


class TestGenreSuccessful:

    #Получение жанров фильмов
    def test_get_all_genres(self,api_manager):
        response = api_manager.movies_api.get_all_genres().json()
        assert response is not None,f'Expected: Not None, Received:{response}'

    #Создание жанра
    def test_create_genre(self, create_new_genre, test_genre):
        created_genre_name = create_new_genre.get('name')
        assert test_genre.get('name') == created_genre_name

    #Удаление жанра
    def test_delete_genre(self,super_admin,create_new_genre):
        created_genre_id = create_new_genre.get('id')
        super_admin.api.movies_api.delete_genre_by_id(created_genre_id)
        super_admin.api.movies_api.get_genre_by_id(created_genre_id,expected_status=404)

    #Получение жанра по ID
    def test_get_genre_by_id (self,super_admin,create_new_genre,test_genre):
        created_genre_id = create_new_genre.get('id')
        get_genre_by_id_response = super_admin.api.movies_api.get_genre_by_id(created_genre_id).json()
        assert get_genre_by_id_response.get('id') == created_genre_id
        assert get_genre_by_id_response.get('name') == test_genre.get('name')


class TestMoviesNegative:

    @allure.epic("Movies api")
    @allure.story("Negative")
    @allure.description("Этот тест проверяет, что при передаче не корректного параметра (pageSize = 0) в запросе GET/movies отдает ошибку 400")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Негативный тест GET/ movies c не валидным параметром")
    @pytest.mark.smoke
    def test_get_movies_with_wrong_params(self,api_manager):
        with allure.step("Вызываем метод GET/movies с параметром pageSize = 0"):
            response = api_manager.movies_api.get_movies(expected_status=400,params={'pageSize':0})
            error_data = response.json()
        with allure.step("Проверяем наличие сообщения в ответе"):
            assert "message" in  error_data, "Expected: 'message' in response, received: no 'message' in response"
            messages = error_data["message"]
        with allure.step("Проверяем что сообщение об  ошибке - массив"):
            assert isinstance(messages,list), " 'message' is not list"
        with allure.step("Проверяем, что текст ошибки корректный"):
            assert messages[0] == "Поле pageSize имеет минимальную величину 1", f"Unexpected message: {messages[0]}"

    @allure.epic("Movies api")
    @allure.story("Negative")
    @allure.description("Этот тест проверяет, что при передаче не корректного тела (Отсутсвует поле name) в запросе POST/movies отдает ошибку 400")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Негативный тест POST/ movies c не валидным телом")
    @pytest.mark.smoke
    def test_create_movie_with_wrong_body(self,incorrect_test_movie,super_admin):
        with allure.step("Отправляем запрос с не валидным телом"):
            response = super_admin.api.movies_api.create_movie(incorrect_test_movie,expected_status=400)
            error_data = response.json()
        with allure.step("Проверяем налиичие сообщения в отете"):
            assert "message" in error_data, "Expected: 'message' in response, received: no 'message' in response"
            messages = error_data["message"]
        with allure.step("Проверяем что сообщение об  ошибке - массив"):
            assert isinstance(messages, list), " 'message' is not list"
        with allure.step("Проверяем, что текст ошибки корректный"):
            assert messages[0] == "name should not be empty", f"Unexpected message: {messages[0]}"

    @allure.epic("Movies api")
    @allure.story("Negative")
    @allure.description("Этот тест проверяет, что при передаче отрицательного ID  в запросе GET/movies/{id} отдает ошибку 404")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Негативный тест GET/ movies/{id} c отрицательным ID")
    @pytest.mark.smoke
    def test_get_movie_by_id_with_negative_id(self,api_manager):
        with allure.step("Вызываем метод GET/ movies/{id} c отрицательным ID"):
            response = api_manager.movies_api.get_movie_by_id(-1,expected_status=404)
            error_data = response.json()
        with allure.step("Проверяем наличие поля message в ответе"):
            assert "message" in error_data
        with allure.step("Проверяем наличие поля error в ответе"):
            assert "error" in error_data
        with allure.step("Проверяем корректность значения поля message"):
            assert error_data["message"] == "Фильм не найден", f"Unexpected message: {error_data["message"]}"
        with allure.step("Проверяем корректность значения поля error"):
            assert error_data["error"] == "Not Found", f"Unexpected error: {error_data["error"]}"

    @allure.epic("Movies api")
    @allure.story("Negative")
    @allure.description("Этот тест проверяет, что при передаче отрицательного ID  в запросе DELETE/movies/{id} отдает ошибку 404")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Негативный тест DELETE/ movies/{id} c отрицательным ID")
    @pytest.mark.smoke
    def test_delete_movie_by_id_with_negative_id(self,super_admin):
        with allure.step("Вызываем метод DELETE/ movies/{id} c отрицательным ID"):
            response = super_admin.api.movies_api.delete_movie_by_id(-1,expected_status=404)
            error_data = response.json()
        with allure.step("Проверяем наличие поля message в ответе"):
            assert "message" in error_data
        with allure.step("Проверяем наличие поля error в ответе"):
            assert "error" in error_data
        with allure.step("Проверяем корректность значения поля message"):
            assert error_data["message"] == "Фильм не найден", f"Unexpected message: {error_data["message"]}"
        with allure.step("Проверяем корректность значения поля error"):
            assert error_data["error"] == "Not Found", f"Unexpected error: {error_data["error"]}"

    @allure.epic("Movies api")
    @allure.story("Negative")
    @allure.description("Этот тест проверяет, что при передаче отрицательного ID  в запросе PATCH/movies/{id} отдает ошибку 404")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Негативный тест PATCH/ movies/{id} c отрицательным ID")
    @pytest.mark.smoke
    def test_edit_movie_by_id_with_negative_id(self, super_admin):
        with allure.step("Вызываем метод PATCH/ movies/{id} c отрицательным ID"):
            response = super_admin.api.movies_api.edit_movie_by_id(-1,data= {},expected_status=404)
            error_data = response.json()
        with allure.step("Проверяем наличие поля message в ответе"):
            assert "message" in error_data
        with allure.step("Проверяем наличие поля error в ответе"):
            assert "error" in error_data
        with allure.step("Проверяем корректность значения поля message"):
            assert error_data["message"] == "Фильм не найден", f"Unexpected message: {error_data["message"]}"
        with allure.step("Проверяем корректность значения поля error"):
            assert error_data["error"] == "Not Found", f"Unexpected error: {error_data["error"]}"

    @allure.epic("Movies api")
    @allure.story("Negative")
    @allure.description("Этот тест проверяет, что при передаче созданиии фильма пользователем с ролью USER отдает ошибку 403")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title(" POST/movies с ролью USER")
    @pytest.mark.smoke
    def test_create_movie_by_common_user(self,common_user,test_movie):
        with allure.step("Отправляем запрос и проверяем статус код"):
            response = common_user.api.movies_api.create_movie(test_movie,expected_status=403)

