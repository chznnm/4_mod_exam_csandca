from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_BASE_URL

MOVIES = '/movies'
REVIEWS = '/reviews'
GENRES = '/genres'

class MoviesApi(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url = MOVIES_BASE_URL)

    #Получение афиш фильмов
    def get_movies(self, expected_status = 200, **kwargs):
        return self.send_request(
            method = "GET",
            endpoint = MOVIES,
            expected_status = expected_status,
            **kwargs
        )

    #Создание фильма
    def create_movie(self,data, expected_status = 201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=MOVIES,
            data=data,
            expected_status=expected_status,
            **kwargs
        )

    #Получение фильма по ID
    def get_movie_by_id(self,movie_id,expected_status=200,**kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{movie_id}",
            expected_status=expected_status,
            **kwargs
        )

    #Удаление фильма по ID
    def delete_movie_by_id(self,movie_id,expected_status=200,**kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{movie_id}",
            expected_status=expected_status,
            **kwargs
        )

    #Редактирование фильма по ID
    def edit_movie_by_id(self,movie_id,data,expected_status=200,**kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie_id}",
            data=data,
            expected_status=expected_status,
            **kwargs
        )

    #Получение отзывов фильма
    def get_reviews_by_movie_id(self,movie_id,expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{movie_id}{REVIEWS}",
            expected_status = expected_status,
            **kwargs
        )

    #Создание отзыва к фильму по ID
    def create_review_for_movie(self,movie_id,data,expected_status=201,**kwargs):
        return self.send_request(
            method="POST",
            endpoint=f"{MOVIES}/{movie_id}{REVIEWS}",
            data=data,
            expected_status=expected_status,
            **kwargs
        )

    #Редактирование отзыва к фильму
    def edit_review_by_movie_id(self,movie_id,data,expected_status=200,**kwargs):
        return self.send_request(
            method="PUT",
            endpoint=f"{MOVIES}/{movie_id}{REVIEWS}",
            data=data,
            expected_status=expected_status,
            **kwargs
        )

    #Удаление отзыва к фильму
    def delete_review_by_movie_id(self,movie_id,user_id,expected_status=200,**kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{movie_id}{REVIEWS}",
            params=user_id,
            expected_status=expected_status,
            **kwargs
        )

    #Скрыть отзыв к фильму
    def hide_review_by_movie_id(self,movie_id,user_id,expected_status=200,**kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie_id}{REVIEWS}/hide/{user_id}",
            expected_status=expected_status,
            **kwargs
        )

    #Показать отзыв к фильму
    def show_review_by_movie_id(self,movie_id,user_id,expected_status=200,**kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie_id}{REVIEWS}/show/{user_id}",
            expected_status=expected_status,
            **kwargs
        )

    #Получение жанров фильмов
    def get_all_genres(self,expected_status=200,**kwargs):
        return self.send_request(
            method="GET",
            endpoint=GENRES,
            expected_status=expected_status,
            **kwargs
        )

    #Создание жанра
    def create_new_genre(self,data,expected_status=201,**kwargs):
        return self.send_request(
            method="POST",
            endpoint=GENRES,
            data=data,
            expected_status=expected_status,
            **kwargs
        )

    #Удаление жанра
    def delete_genre_by_id(self,genre_id,expected_status=200,**kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f'{GENRES}/{genre_id}',
            expected_status=expected_status,
            **kwargs
        )

    #Получение жанра по ID
    def get_genre_by_id(self,genre_id,expected_status=200,**kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{GENRES}/{genre_id}",
            expected_status=expected_status,
            **kwargs
        )