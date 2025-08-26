from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    # Корзина в хедере
    CART_LINK = (By.ID, "shopping_cart_container")

    # Кнопки добавления по data-test
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_BOLT_TSHIRT = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    ADD_ONESIE = (By.ID, "add-to-cart-sauce-labs-onesie")

    def add_three_items(self):
        self.click(self.ADD_BACKPACK)
        self.click(self.ADD_BOLT_TSHIRT)
        self.click(self.ADD_ONESIE)

    def open_cart(self):
        self.click(self.CART_LINK)