from pages.base_page import BasePage

class AllMoviesBasePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = f"{self.home_url}movies"

        self.more_button ='[data-qa-id="more_button"]'

    def open(self):
        self.open_url(self.url)

    def go_to_movie(self):
        self.click(self.more_button)
