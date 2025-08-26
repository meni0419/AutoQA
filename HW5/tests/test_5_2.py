from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_drag_first_photo_to_trash(driver):
    driver.get("https://www.globalsqa.com/demo-site/draganddrop/")
    wait = WebDriverWait(driver, 40)

    # Страница встраивает демо в iframe — переключаемся
    demo_iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.demo-frame")))
    driver.switch_to.frame(demo_iframe)

    # Дождаться загрузки галереи и корзины
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#gallery")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#trash")))

    # Иногда элементы инициализируются jQuery UI с задержкой — ждём, пока элементы станут видимыми
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#gallery > li")) >= 1)

    # Первая фотография (верхний левый элемент)
    first_photo = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#gallery > li")))
    trash = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#trash")))

    # Подсчёт до перетаскивания
    def counts():
        gallery_items = driver.find_elements(By.CSS_SELECTOR, "#gallery > li")
        trash_items = driver.find_elements(By.CSS_SELECTOR, "#trash li")
        return len(gallery_items), len(trash_items)

    gallery_before, trash_before = counts()

    # Перетаскивание (jQuery UI хорошо работает с классическим drag_and_drop)
    actions = ActionChains(driver)
    actions.drag_and_drop(first_photo, trash).perform()

    # Подождать, пока элемент переместится (изменится количество в списках)
    wait.until(lambda d: counts() != (gallery_before, trash_before))

    gallery_after, trash_after = counts()

    # Проверки по заданию:
    # - в корзине появилась одна фотография (trash увеличился на 1)
    # - в галерее стало на одну меньше; ожидаемо 3 (если исходно было 4)
    assert trash_after == trash_before + 1, f"Ожидалось, что в корзине станет на 1 фото больше. Было: {trash_before}, стало: {trash_after}"
    if gallery_before >= 4:
        assert gallery_after == 3, f"Ожидалось, что в галерее останется 3 фото, получено: {gallery_after}"
    else:
        # На случай, если демо грузится с иным начальными данными — проверяем относительное изменение
        assert gallery_after == gallery_before - 1, f"Галерея должна уменьшиться на 1. Было: {gallery_before}, стало: {gallery_after}"

    # Вернуться в основной контент
    driver.switch_to.default_content()