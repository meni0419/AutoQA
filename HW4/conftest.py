import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

try:
    from webdriver_manager.firefox import GeckoDriverManager  # type: ignore
    USE_WDM = True
except Exception:
    USE_WDM = False


@pytest.fixture(scope="session")
def driver():
    options = FirefoxOptions()
    options.add_argument("-headless")  # уберите, если хотите видеть браузер

    if USE_WDM:
        service = FirefoxService(GeckoDriverManager().install())
    else:
        service = FirefoxService()  # geckodriver должен быть в PATH

    drv = webdriver.Firefox(service=service, options=options)
    drv.set_window_size(1440, 900)
    yield drv
    drv.quit()