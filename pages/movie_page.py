from pages.base_page import BasePage
from utils.data_generator import DataGenerator
class MovieBasePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.buy_ticket_button = '[data-qa-id="movie_buy_ticket_button"]'
        self.review_input = '[data-qa-id="movie_review_input"]'
        self.send_button = '[data-qa-id="movie_review_submit_button"]'
        self.rating_input =  '[data-qa-id="movie_rating_select"]'

    def create_review(self,review_data,review_rating):
        self.enter_text(self.review_input, review_data)
        self.click(self.rating_input)
        self.page.get_by_role("option", name=review_rating).click()
        self.click(self.send_button)
