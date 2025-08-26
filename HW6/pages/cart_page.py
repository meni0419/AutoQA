from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    CHECKOUT_BTN = (By.ID, "checkout")  # data-test="checkout"

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BTN)