from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, base_url="https://www.saucedemo.com"):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self, path=""):
        url = f"{self.base_url}/{path.lstrip('/')}"
        self.driver.get(url)

    def wait_visible(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def click(self, locator, timeout=20):
        self.wait_clickable(locator, timeout).click()

    def type(self, locator, text, timeout=20, clear=True):
        el = self.wait_visible(locator, timeout)
        if clear:
            el.clear()
        el.send_keys(text)
        return el