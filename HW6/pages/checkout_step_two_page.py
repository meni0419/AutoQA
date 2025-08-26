from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutStepTwoPage(BasePage):
    TOTAL_LABEL = (By.CSS_SELECTOR, "[data-test='total-label']")  # "Total: $58.29"

    def get_total_text(self) -> str:
        return self.wait_visible(self.TOTAL_LABEL).text.strip()