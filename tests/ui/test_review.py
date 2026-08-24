import allure
import pytest
from playwright.sync_api import expect


@allure.epic("Тестирование UI")
@allure.feature("Написание отзыва")
@pytest.mark.ui
class TestReview:
    @allure.title("Успешное написание отзыва пользователя")
    def test_create_review(self,login_page,register_page,all_movies_page,base_page,movie_page, registered_user,test_review, page):
        review_body = test_review.get("text")
        review_rating = str(test_review.get("rating"))
        with allure.step("Открываем главную страницу"):
            base_page.open()
        with allure.step("Авторизируемся"):
            base_page.go_to_login()
            login_page.login(registered_user.email,registered_user.password)
        with allure.step("Проверяем успешный вход"):
            expect(page.get_by_text("Вы вошли в аккаунт")).to_be_visible()
        with allure.step("Переходим ко всем фильмам"):
            base_page.go_to_all_movies()
        with allure.step("Пишем отзыв"):
            all_movies_page.go_to_movie()
            movie_page.create_review(review_body,review_rating)
        with allure.step("Проверяем наличие уведомления об успешном создании отзыва"):
            expect(page.get_by_text("Отзыв успешно создан")).to_be_visible()
        with allure.step("Проверяем, что данные в отзыве корректны"):
            expect(page.get_by_text(registered_user.fullName)).to_be_visible()
            expect(page.get_by_text(review_body)).to_be_visible()
            rating_xpath = f"//h4[normalize-space()='{registered_user.fullName}']/following::h3[1]"
            expect(page.locator(rating_xpath)).to_be_visible(timeout=10000)
        with allure.step("Прибираемся за собой"):
            movie_page.delete_review()
        with allure.step("Проверяем, что отзыв удален"):
            expect(page.get_by_text("Отзыв успешно удален")).to_be_visible()

