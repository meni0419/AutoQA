import os
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

try:
    from webdriver_manager.firefox import GeckoDriverManager  # type: ignore
    USE_WDM = True
except Exception:
    USE_WDM = False

def pytest_addoption(parser):
    parser.addoption("--base-url", action="store",
                     default=os.environ.get("BASE_URL", "https://www.saucedemo.com"),
                     help="Base URL for saucedemo")

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("--base-url")

@pytest.fixture(scope="session")
def driver():
    options = FirefoxOptions()
    options.add_argument("-headless")  # уберите, чтобы видеть окно
    if USE_WDM:
        service = FirefoxService(GeckoDriverManager().install())
    else:
        service = FirefoxService()
    drv = webdriver.Firefox(service=service, options=options)
    drv.set_window_size(1440, 900)
    yield drv
    drv.quit()