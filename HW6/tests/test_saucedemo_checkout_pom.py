import re
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage

def extract_amount(total_text: str) -> str:
    # Ожидаемый формат: "Total: $58.29"
    m = re.search(r"\$\d+\.\d{2}", total_text)
    return m.group(0) if m else total_text

def test_checkout_total_with_pom(driver, base_url):
    # 1-2) Логин
    login = LoginPage(driver, base_url)
    login.open_login()
    login.login_as("standard_user", "secret_sauce")

    # 3) Добавить 3 товара
    inventory = InventoryPage(driver, base_url)
    inventory.add_three_items()

    # 4) Открыть корзину
    inventory.open_cart()
    cart = CartPage(driver, base_url)

    # 5) Checkout
    cart.proceed_to_checkout()

    # 6) Заполнить данные
    step1 = CheckoutStepOnePage(driver, base_url)
    step1.fill_and_continue(first="Max", last="Melnychuk", postal="69035")

    # 7) Прочитать Total
    step2 = CheckoutStepTwoPage(driver, base_url)
    total_text = step2.get_total_text()
    total_amount = extract_amount(total_text)

    # 8) Закрытие браузера обеспечивается фикстурой драйвера (teardown)

    # 9) Проверка Total
    assert total_amount == "$58.29", f"Ожидалось '$58.29', получено: '{total_text}'"