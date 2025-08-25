from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_41_text_input_button_change(driver):
    wait = WebDriverWait(driver, 20)
    driver.get("http://uitestingplayground.com/textinput")

    # Вводим текст в поле
    input_box = wait.until(EC.element_to_be_clickable((By.ID, "newButtonName")))
    input_box.clear()
    input_box.send_keys("ITCH")

    # Кликаем по синей кнопке
    button = wait.until(EC.element_to_be_clickable((By.ID, "updatingButton")))
    button.click()

    # Ожидаем, пока текст кнопки обновится
    wait.until(lambda d: d.find_element(By.ID, "updatingButton").text.strip() == "ITCH")
    assert driver.find_element(By.ID, "updatingButton").text.strip() == "ITCH", "Текст кнопки не изменился на 'ITCH'"
