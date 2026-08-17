import allure

from pages.actions import PageAction

class BasePage(PageAction):
    def __init__(self, page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"
        self.all_movies_link = 'a[href="/movies"]'
        self.profile_link = 'a[href="/profile"]'
        self.login_link = 'a[href="/login"]'

    @allure.step("Переход на 'Все фильмы' из шапки")
    def go_to_all_movies(self):
        self.click(self.all_movies_link)

    @allure.step("Переход в Профиль из шапки")
    def go_to_profile(self):
        self.click(self.profile_link)

    @allure.step("Переход на 'Войти' из шапки")
    def go_to_login(self):
        self.click(self.login_link)

    def open(self):
        self.open_url(self.home_url)