from pages.base_page import BasePage

class CinescopeLoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = f"{self.home_url}login"
        self.register_link = 'a[href="/register"]'

        self.email_input = '[data-qa-id="login_email_input"]'
        self.password_input ='[data-qa-id="login_password_input"]'
        self.submit_button ='[data-qa-id="login_submit_button"]'

    def open(self):
        self.open_url(self.url)

    def login(self,email: str, password: str):
        self.enter_text(self.email_input,email)
        self.enter_text(self.password_input,password)
        self.click(self.submit_button)

    def go_to_register_from_login_page(self):
        self.click(self.register_link)