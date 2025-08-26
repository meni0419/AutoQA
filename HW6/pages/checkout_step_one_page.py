from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutStepOnePage(BasePage):
    FIRST_NAME = (By.ID, "first-name")   # data-test="firstName"
    LAST_NAME = (By.ID, "last-name")     # data-test="lastName"
    POSTAL_CODE = (By.ID, "postal-code") # data-test="postalCode"
    CONTINUE_BTN = (By.ID, "continue")   # data-test="continue"

    def fill_and_continue(self, first: str, last: str, postal: str):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)
        self.click(self.CONTINUE_BTN)