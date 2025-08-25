from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_42_loading_images_alt_attribute(driver):
    wait = WebDriverWait(driver, 20)
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")

    # Дождаться индикатора "Done!"
    wait.until(EC.text_to_be_present_in_element((By.ID, "text"), "Done!"))

    # Дополнительно дождаться, что все изображения загружены (naturalWidth > 0)
    def all_images_loaded(d):
        return d.execute_script("""
            const imgs = document.querySelectorAll('#image-container img');
            if (!imgs.length) return false;
            return Array.from(imgs).every(img => img.complete && img.naturalWidth > 0);
        """)
    wait.until(all_images_loaded)

    # Получить alt третьего изображения
    third_img = driver.find_element(By.CSS_SELECTOR, "#image-container img:nth-of-type(3)")
    alt_value = third_img.get_attribute("alt")
    assert alt_value == "award", f"Ожидался alt='award', получено: {alt_value!r}"