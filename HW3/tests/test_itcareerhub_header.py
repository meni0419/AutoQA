from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_header_elements_and_phone_popup(driver, base_url):
    wait = WebDriverWait(driver, 30)
    driver.get(base_url)

    # 1) Дождаться полной загрузки страницы
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    # 2) Проверка элементов в шапке:
    # Логотип ITCareerHub (img с alt="IT Career Hub")
    logo_img = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='IT Career Hub']"))
    )
    assert logo_img.is_displayed(), "Логотип не отображается"

    # Ссылка “Программы” — избегаем XPath, используем LINK_TEXT
    programs_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Программы")))
    assert programs_link.is_displayed(), "Ссылка 'Программы' не отображается"

    # Ссылка “Способы оплаты”
    payments_link = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.tn-atom[href='#rec717852307']"))
    )
    assert payments_link.is_displayed(), "Ссылка 'Способы оплаты' не отображается"

    # Ссылка “Новости”
    news_link = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.tn-atom[href='#rec725283886']"))
    )
    assert news_link.is_displayed(), "Ссылка 'Новости' не отображается"

    # Ссылка “О нас”
    about_link = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.tn-atom[href='#rec717852887']"))
    )
    assert about_link.is_displayed(), "Ссылка 'О нас' не отображается"

    # Ссылка “Отзывы”
    reviews_link = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.tn-atom[href='/reviews']"))
    )
    assert reviews_link.is_displayed(), "Ссылка 'Отзывы' не отображается"

    # Кнопки языка: ru и de — только CSS, без XPath
    ru_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.tn-atom[href='/ru']")))
    assert ru_link.is_displayed() and ru_link.text.strip().lower() == "ru", \
        "Ссылка переключения языка 'ru' не отображается"

    de_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']")))
    assert de_link.is_displayed() and de_link.text.strip().lower() == "de", \
        "Ссылка переключения языка 'de' не отображается"

    # 3) Проверка переключения языка: RU -> DE
    de_link.click()

    # Ждём перехода на корень (DE), перезагрузку и смену языка
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    wait.until(EC.url_matches(r"https://itcareerhub\.de/?$"))

    # Пытаемся подтвердить DE несколькими способами (надёжнее, чем просто URL):
    #  - lang=de в <html>
    #  - наличие немецкой версии пункта меню "Programme"
    #  - отсутствие русской версии "Программы"
    def get_html_lang(d):
        return (d.execute_script(
            "return document.documentElement.lang || document.documentElement.getAttribute('lang') || ''") or "").lower()

    lang_attr = get_html_lang(driver)
    if lang_attr:
        assert lang_attr.startswith("de"), f"Ожидался lang='de', а получили: {lang_attr}"

    # Если на странице есть немецкий пункт "Programme", проверим его
    try:
        programmes_de = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Programme"))
        )
        assert programmes_de.is_displayed(), "Немецкий пункт меню 'Programme' не отображается"
    except Exception:
        # убедимся, что русской версии нет
        elems_ru = driver.find_elements(By.LINK_TEXT, "Программы")
        assert len(elems_ru) == 0, "Похоже язык не переключился — на странице всё ещё виден пункт 'Программы'"

    # 4) Переключение обратно: DE -> RU
    ru_link_de_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.tn-atom[href='/ru']")))
    ru_link_de_page.click()
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    wait.until(EC.url_contains("/ru"))

    # Подтверждаем возврат на RU:
    lang_attr_back = get_html_lang(driver)
    if lang_attr_back:
        assert lang_attr_back.startswith("ru"), f"Ожидался lang='ru', а получили: {lang_attr_back}"

    # Ищем русскую версию пункта меню
    programs_link_back = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Программы")))
    assert programs_link_back.is_displayed(), "После переключения обратно пункт 'Программы' не отображается"

    # 5) Клик по иконке с телефонной трубкой
    phone_icon = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.tn-atom[href='#popup:form-tr3']"))
    )
    phone_icon.click()

    # 6) Проверка текста в попапе — без XPath:
    expected_text = "Если вы не дозвонились, заполните форму на сайте. Мы свяжемся с вами"

    # Ждём, пока появится видимый попап (у Tilda это обычно .t-popup_show)
    popup_container = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".t-popup.t-popup_show, .t702__popup.t-popup_show"))
    )
    # Проверяем текст целиком по контейнеру попапа
    assert expected_text in popup_container.text, "Ожидаемый текст в попапе не найден"
