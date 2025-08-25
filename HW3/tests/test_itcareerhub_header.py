from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_header_elements_and_phone_popup(driver, base_url):
    wait = WebDriverWait(driver, 30)
    driver.get(base_url)

    # 1) Дождаться, что DOM загружен
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    # 2) Проверка элементов в шапке:
    # Логотип ITCareerHub (img с alt="IT Career Hub")
    logo_img = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "img[alt='IT Career Hub']")))
    assert logo_img.is_displayed(), "Логотип не отображается"

    # Ссылка “Программы” (текст)
    programs_link = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[normalize-space()='Программы' or contains(normalize-space(.),'Программы')]")))
    assert programs_link.is_displayed(), "Ссылка 'Программы' не отображается"

    # Ссылка “Способы оплаты”
    payments_link = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a.tn-atom[href='#rec717852307']")))
    assert payments_link.is_displayed(), "Ссылка 'Способы оплаты' не отображается"

    # Ссылка “Новости”
    news_link = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a.tn-atom[href='#rec725283886']")))
    assert news_link.is_displayed(), "Ссылка 'Новости' не отображается"

    # Ссылка “О нас”
    about_link = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a.tn-atom[href='#rec717852887']")))
    assert about_link.is_displayed(), "Ссылка 'О нас' не отображается"

    # Ссылка “Отзывы”
    reviews_link = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a.tn-atom[href='/reviews']")))
    assert reviews_link.is_displayed(), "Ссылка 'Отзывы' не отображается"

    # Кнопки языка: ru и de
    ru_link = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[@href='/ru' and normalize-space()='ru']")))
    assert ru_link.is_displayed(), "Ссылка переключения языка 'ru' не отображается"

    de_link = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[@href='/' and normalize-space()='de']")))
    assert de_link.is_displayed(), "Ссылка переключения языка 'de' не отображается"

    # 3) Клик по иконке с телефонной трубкой
    phone_icon = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.tn-atom[href='#popup:form-tr3']")))
    phone_icon.click()

    # 4) Проверка текста в попапе
    expected_text = "Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами"
    popup_text = wait.until(EC.visibility_of_element_located((
        By.XPATH,
        f"//*[contains(@class,'tn-atom')][contains(normalize-space(text()),\"{expected_text}\")]"
    )))
    assert expected_text in popup_text.text, "Ожидаемый текст в попапе не найден"