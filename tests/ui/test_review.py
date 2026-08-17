from random import randint
import allure
import pytest
import re
from playwright.sync_api import expect


@allure.epic("Тестирование UI")
@allure.feature("Написание отзыва")
@pytest.mark.ui

class TestReview:
    @allure.title("Успешное написание отзыва пользователя")
    def test_create_review(self,login_page,register_page,all_movies_page,base_page,movie_page, test_user,test_review, page):
        review_body = test_review.get("text")
        review_rating = str(test_review.get("rating"))
        base_page.open()
        base_page.go_to_login()
        login_page.go_to_register_from_login_page()
        register_page.register(test_user.fullName, test_user.email, test_user.password)
        expect(page.get_by_text("Подтвердите свою почту")).to_be_visible()
        login_page.login(test_user.email,test_user.password)
        expect(page.get_by_text("Что-то пошло не так")).to_be_visible()
        # Т.к сейчас редиректа на главную страницу не происходит перезагружаем страницу
        page.reload()
        base_page.go_to_all_movies()
        all_movies_page.go_to_movie()
        movie_page.create_review(review_body,review_rating)
        expect(page.get_by_text("Отзыв успешно создан")).to_be_visible()
        expect(page.get_by_text(test_user.fullName)).to_be_visible()
        expect(page.get_by_text(review_body)).to_be_visible()
        rating_xpath = f"//h4[normalize-space()='{test_user.fullName}']/following::h3[1]"
        expect(page.locator(rating_xpath)).to_be_visible(timeout=10000)



