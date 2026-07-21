import pytest
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
    @pytest.mark.parametrize("role,status_code",[
        ("super_admin",200),
        ("admin",403),
        ("common_user",403)
    ])
    def  test_delete_movie_by_id(self,request,super_admin,create_new_movie, test_movie,role,status_code):
        created_movie_id = create_new_movie.get("id")
        if role == "super_admin":
            current_user = super_admin
        else:
            current_user = request.getfixturevalue(role)
        delete_movie_response = current_user.api.movies_api.delete_movie_by_id(created_movie_id,expected_status=status_code).json()
        if status_code == 200:
            assert_movie_data_matches(test_movie,delete_movie_response)
            current_user.api.movies_api.get_movie_by_id(created_movie_id,expected_status=404)
        else:
            current_user.api.movies_api.get_movie_by_id(created_movie_id,expected_status=200)

    #Редактирование фильма по ID
    def test_edit_created_movie_by_id(self,super_admin,create_new_movie,test_movie):
        created_movie_id = create_new_movie.get("id")
        edited_movie_response = super_admin.api.movies_api.edit_movie_by_id(created_movie_id,generate_edited_movie_data()).json()
        get_response = super_admin.api.movies_api.get_movie_by_id(created_movie_id).json()
        assert edited_movie_response["name"] == get_response["name"],f'Expected:{edited_movie_response['name']}, Received:{get_response['name']}'
        assert edited_movie_response["price"] == get_response["price"],f'Expected:{edited_movie_response['price']}, Received:{get_response['price']}'
        assert test_movie["imageUrl"] == get_response["imageUrl"],f'Expected:{edited_movie_response['imageUrl']}, Received:{get_response['imageUrl']}'
        assert test_movie["description"] == get_response["description"],f'Expected:{edited_movie_response['description']}, Received:{get_response['description']}'
        assert test_movie["location"] == get_response["location"],f'Expected:{edited_movie_response['location']}, Received:{get_response['location']}'
        assert test_movie["published"] == get_response["published"],f'Expected:{edited_movie_response['published']}, Received:{get_response['published']}'

    #Проверка фильтров получения фильмов(Параметризиированный)
    @pytest.mark.parametrize("min_price,max_price,locations,genre_id",[
        (1,500,["MSK"],4),
        (501,1000,["SPB"],5),
        (1,1000,['MSK','SPB'],4)
    ])
    def test_get_all_movies_with_parametrize(self,super_admin,min_price,max_price,locations,genre_id):
        params = {
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": locations,
            "genreId": genre_id
        }
        response = super_admin.api.movies_api.get_movies(expected_status=200,params = params).json()
        assert response['movies'],"No movies found"
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

    #Получение афиш фильмов с не корректным параметром
    def test_get_movies_with_wrong_params(self,api_manager):
        response = api_manager.movies_api.get_movies(expected_status=400,params={'pageSize':0})
        error_data = response.json()
        assert "message" in  error_data, "Expected: 'message' in response, received: no 'message' in response"
        messages = error_data["message"]
        assert isinstance(messages,list), " 'message' is not list"
        assert messages[0] == "Поле pageSize имеет минимальную величину 1", f"Unexpected message: {messages[0]}"

    #Создание фильма с неверным телом запроса (Отсутсвует поле "name")
    def test_create_movie_with_wrong_body(self,incorrect_test_movie,super_admin):
        response = super_admin.api.movies_api.create_movie(incorrect_test_movie,expected_status=400)
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
    def test_delete_movie_by_id_with_negative_id(self,super_admin):
        response = super_admin.api.movies_api.delete_movie_by_id(-1,expected_status=404)
        error_data = response.json()
        assert "message" in error_data
        assert "error" in error_data
        assert error_data["message"] == "Фильм не найден", f"Unexpected message: {error_data["message"]}"
        assert error_data["error"] == "Not Found", f"Unexpected error: {error_data["error"]}"


    # Редактирование фильма по ID, с отрицательным ID
    def test_edit_movie_by_id_with_negative_id(self, super_admin):
        response = super_admin.api.movies_api.edit_movie_by_id(-1,data= {},expected_status=404)
        error_data = response.json()
        assert "message" in error_data
        assert "error" in error_data
        assert error_data["message"] == "Фильм не найден", f"Unexpected message: {error_data["message"]}"
        assert error_data["error"] == "Not Found", f"Unexpected error: {error_data["error"]}"

    def test_create_movie_by_common_user(self,common_user,test_movie):
        response = common_user.api.movies_api.create_movie(test_movie,expected_status=403)
