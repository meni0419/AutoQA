from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")         # data-test="username"
    PASSWORD = (By.ID, "password")          # data-test="password"
    LOGIN_BTN = (By.ID, "login-button")     # data-test="login-button"

    def open_login(self):
        self.open("/")

    def login_as(self, username: str, password: str):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)