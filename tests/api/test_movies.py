
from  tests.helpers.assertions import assert_movie_data_matches,assert_review_data_matches
from data.movie.movie_data import generate_edited_movie_data, generate_edited_review_data


class TestMoviesSuccessful:

    #Получение афиш фильмов без параметров
    def test_get_movies(self,api_manager):
        response = api_manager.movies_api.get_movies().json()
        assert response.get('movies') is not  None

    #Получение афиш фильмов с фильтрами (Проверяет только 1 страницу, можно либо в цикле вызывать все страницы пока не получим пустой список, либо передавать limit с большим значением)
    def test_get_movies_with_params(self,api_manager):
        response = api_manager.movies_api.get_movies(params={'locations':'MSK'}).json()
        for movie in response['movies']:
            assert movie['location'] == 'MSK',f'expected: MSK, received:{movie['location']}'

    #Создание фильма
    def test_create_new_movie(self,api_manager, test_movie,create_new_movie):
        response = create_new_movie
        assert_movie_data_matches(test_movie,response)

    #Получение информации о фильме по ID
    def test_get_movie_by_id(self,api_manager,create_new_movie,test_movie):
        created_movie_id = create_new_movie.get('id')
        get_movie_by_id_response =  api_manager.movies_api.get_movie_by_id(movie_id=created_movie_id).json()
        assert_movie_data_matches(test_movie,get_movie_by_id_response)

    #Удаление фильма по ID
    def  test_delete_movie_by_id(self,api_manager,create_new_movie, test_movie):
        created_movie_id = create_new_movie.get("id")
        delete_movie_response = api_manager.movies_api.delete_movie_by_id(created_movie_id).json()
        assert_movie_data_matches(test_movie,delete_movie_response)
        api_manager.movies_api.get_movie_by_id(created_movie_id,expected_status=404)

    #Редактирование фильма по ID
    def test_edit_created_movie_by_id(self,api_manager,create_new_movie,test_movie):
        created_movie_id = create_new_movie.get("id")
        edited_movie_response = api_manager.movies_api.edit_movie_by_id(created_movie_id,generate_edited_movie_data()).json()
        get_response = api_manager.movies_api.get_movie_by_id(created_movie_id).json()
        assert edited_movie_response["name"] == get_response["name"],f'Expected:{edited_movie_response['name']}, Received:{get_response['name']}'
        assert edited_movie_response["price"] == get_response["price"],f'Expected:{edited_movie_response['price']}, Received:{get_response['price']}'
        assert test_movie["imageUrl"] == get_response["imageUrl"],f'Expected:{edited_movie_response['imageUrl']}, Received:{get_response['imageUrl']}'
        assert test_movie["description"] == get_response["description"],f'Expected:{edited_movie_response['description']}, Received:{get_response['description']}'
        assert test_movie["location"] == get_response["location"],f'Expected:{edited_movie_response['location']}, Received:{get_response['location']}'
        assert test_movie["published"] == get_response["published"],f'Expected:{edited_movie_response['published']}, Received:{get_response['published']}'

class TestReviewsSuccessful:

    #Получение отзывов фильма по ID
    def test_get_all_reviews(self,api_manager,create_new_movie):
        created_movie_id = create_new_movie.get('id')
        api_manager.movies_api.get_reviews_by_movie_id(created_movie_id)

    #Создание отзыва к фильму
    def test_create_review(self,api_manager,create_new_review,test_review):
        response = create_new_review
        assert_review_data_matches(test_review,response)

    #Редактирование отзыва к фильму
    def test_edit_review(self,api_manager,create_new_review,create_new_movie):
        created_movie_id = create_new_movie.get('id')
        edited_review_data = generate_edited_review_data()
        edited_review_response = api_manager.movies_api.edit_review_by_movie_id(created_movie_id,edited_review_data).json()
        assert_review_data_matches(edited_review_data,edited_review_response)
        get_review_response = api_manager.movies_api.get_reviews_by_movie_id(created_movie_id).json()
        user_id = create_new_review.get('userId')
        found_review = None
        for review in get_review_response:
            if review.get('userId') == user_id:
                found_review = review
                break
        assert_review_data_matches(edited_review_data,found_review)

    #Удаление отзыва к фильму
    def test_delete_review(self,api_manager,create_new_review, create_new_movie):
        created_movie_id = create_new_movie.get('id')
        user_id = create_new_review.get('userId')
        api_manager.movies_api.delete_review_by_movie_id(created_movie_id,user_id)
        get_review_response = api_manager.movies_api.get_reviews_by_movie_id(created_movie_id).json()
        found_review = None
        for review in get_review_response:
            if review.get('userId') == user_id:
                found_review = review
                break
        assert found_review is None, f'Expected: None, received: {found_review}'


"""    #Скрытие отзыва к фильму
    def test_hide_review(self,api_manager,create_new_review,create_new_movie):
        user_id = create_new_review.get('userId')
        created_movie_id = create_new_movie.get('id')
        api_manager.movies_api.hide_review_by_movie_id(created_movie_id,user_id)
        api_manager.movies_api.get_reviews_by_movie_id(created_movie_id)
        
    #Показ отзыва к фильму
    def test_show_review(self,api_manager,create_new_movie,test_review):
        created_movie_id = create_new_movie.get("id")
        user_id = api_manager.movies_api.create_review_for_movie(created_movie_id, test_review).json()['userId']
        api_manager.movies_api.show_review_by_movie_id(created_movie_id,user_id)"""


class TestGenreSuccessful:

    #Получение жанров фильмов
    def test_get_all_genres(self,api_manager):
        response = api_manager.movies_api.get_all_genres().json()
        assert response is not None,f'Expected: Not None, Received:{response}'

    #Создание жанра
    def test_create_genre(self, api_manager, create_new_genre, test_genre):
        created_genre_name = create_new_genre.get('name')
        assert test_genre.get('name') == created_genre_name

    #Удаление жанра
    def test_delete_genre(self,api_manager,create_new_genre):
        created_genre_id = create_new_genre.get('id')
        api_manager.movies_api.delete_genre_by_id(created_genre_id)
        api_manager.movies_api.get_genre_by_id(created_genre_id,expected_status=404)

    #Получение жанра по ID
    def test_get_genre_by_id (self,api_manager,create_new_genre,test_genre):
        created_genre_id = create_new_genre.get('id')
        get_genre_by_id_response = api_manager.movies_api.get_genre_by_id(created_genre_id).json()
        assert get_genre_by_id_response.get('id') == created_genre_id
        assert get_genre_by_id_response.get('name') == test_genre.get('name')


class TestMoviesNegative:

    #Получение афиш фильмов с не корректным параметром
    def test_get_movies_with_wrong_params(self,api_manager):
        response = api_manager.movies_api.get_movies(expected_status=400,params={'pageSize':0})
        error_data = response.json()
        assert "message" in  error_data, "Expected: 'message' in response, received: no 'message' in response"
        messages = error_data["message"]
        assert isinstance(messages,list), " 'message' is not list"
        assert messages[0] == "Поле pageSize имеет минимальную величину 1", f"Unexpected message: {messages[0]}"

    #Создание фильма с неверным телом запроса (Отсутсвует поле "name")
    def test_create_movie_with_wrong_body(self,api_manager,incorrect_test_movie,authenticated_admin):
        response = api_manager.movies_api.create_movie(incorrect_test_movie,expected_status=400)
        error_data = response.json()
        assert "message" in error_data, "Expected: 'message' in response, received: no 'message' in response"
        messages = error_data["message"]
        assert isinstance(messages, list), " 'message' is not list"
        assert messages[0] == "name should not be empty", f"Unexpected message: {messages[0]}"

    #Получение фильма по ID, с отрицательным ID
    def test_get_movie_by_id_with_negative_id(self,api_manager):
        response = api_manager.movies_api.get_movie_by_id(-1,expected_status=404)
        error_data = response.json()
        assert "message" in error_data
        assert "error" in error_data
        assert error_data["message"] == "Фильм не найден", f"Unexpected message: {error_data["message"]}"
        assert error_data["error"] == "Not Found", f"Unexpected error: {error_data["error"]}"

    # Удалениие фильма по ID, с отрицательным ID
    def test_delete_movie_by_id_with_negative_id(self,api_manager,authenticated_admin):
        response = api_manager.movies_api.delete_movie_by_id(-1,expected_status=404)
        error_data = response.json()
        assert "message" in error_data
        assert "error" in error_data
        assert error_data["message"] == "Фильм не найден", f"Unexpected message: {error_data["message"]}"
        assert error_data["error"] == "Not Found", f"Unexpected error: {error_data["error"]}"


    # Редактирование фильма по ID, с отрицательным ID
    def test_edit_movie_by_id_with_negative_id(self,api_manager,authenticated_admin):
        response = api_manager.movies_api.edit_movie_by_id(-1,data= {},expected_status=404)
        error_data = response.json()
        assert "message" in error_data
        assert "error" in error_data
        assert error_data["message"] == "Фильм не найден", f"Unexpected message: {error_data["message"]}"
        assert error_data["error"] == "Not Found", f"Unexpected error: {error_data["error"]}"