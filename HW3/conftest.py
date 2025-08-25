import os
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

try:
    # Упростит установку geckodriver автоматически
    from webdriver_manager.firefox import GeckoDriverManager  # type: ignore
    USE_WDM = True
except Exception:
    USE_WDM = False


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests with visible Firefox window (not headless).",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=os.environ.get("BASE_URL", "https://itcareerhub.de/ru"),
        help="Base URL of the site under test.",
    )


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getoption("--base-url")


@pytest.fixture(scope="session")
def driver(pytestconfig):
    headed = pytestconfig.getoption("--headed")

    options = FirefoxOptions()
    if not headed:
        options.add_argument("-headless")

    if USE_WDM:
        service = FirefoxService(executable_path=GeckoDriverManager().install())
    else:
        service = FirefoxService()  # geckodriver должен быть в PATH

    drv = webdriver.Firefox(service=service, options=options)
    drv.set_page_load_timeout(60)
    drv.set_window_size(1440, 900)
    yield drv
    drv.quit()