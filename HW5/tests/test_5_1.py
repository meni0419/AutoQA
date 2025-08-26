import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_iframe_contains_target_text(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/iframes.html")
    wait = WebDriverWait(driver, 30)

    # 1) Дождаться фрейма и переключиться в него
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#my-iframe")))

    # Контент внутри iframe подгружается через jQuery.load(...), поэтому ждём появления целевого текста
    target_text = "semper posuere integer et senectus justo curabitur."
    elem_with_text = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                f"//*[contains(normalize-space(.), \"{target_text}\")]",
            )
        )
    )

    assert elem_with_text.is_displayed(), "Ожидалось, что текст внутри iframe будет отображаться"

    # Возврат в основной контекст (не обязателен, но полезен для последующих действий в тестах)
    driver.switch_to.default_content()