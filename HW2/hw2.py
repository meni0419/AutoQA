import argparse
import os
import sys
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    # Optional: use webdriver-manager if available (simplifies geckodriver setup)
    from webdriver_manager.firefox import GeckoDriverManager  # type: ignore
    USE_WDM = True
except Exception:
    USE_WDM = False


URL = "https://itcareerhub.de/ru/#rec717852307"
SECTION_SELECTOR = "#rec717852307"


def build_driver(headless: bool) -> webdriver.Firefox:
    options = FirefoxOptions()
    if headless:
        options.add_argument("-headless")

    if USE_WDM:
        service = FirefoxService(executable_path=GeckoDriverManager().install())
    else:
        # Fallback: rely on geckodriver in PATH
        service = FirefoxService()

    driver = webdriver.Firefox(service=service, options=options)
    driver.set_page_load_timeout(60)
    return driver


def take_section_screenshot(output_path: str, headless: bool = True) -> str:
    driver = build_driver(headless=headless)
    try:
        driver.get(URL)

        wait = WebDriverWait(driver, 30)
        section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SECTION_SELECTOR)))

        # Ensure section is in view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", section)

        # Small wait to allow images/webfonts to finish rendering
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        # In case of lazy-loading, give a brief pause
        driver.implicitly_wait(1)

        # Make directories if needed
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        # Screenshot the specific section element
        section.screenshot(output_path)
        return output_path
    finally:
        driver.quit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Take screenshot of 'Способы оплаты' section at itcareerhub.de/ru")
    parser.add_argument(
        "--out",
        default=f"payment_section_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        help="Path to save the screenshot (PNG). Default: payment_section_<timestamp>.png",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run with a visible Firefox window (not headless).",
    )
    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    out_path = os.path.abspath(args.out)
    result = take_section_screenshot(out_path, headless=not args.headed)
    print(f"Saved screenshot to: {result}")


if __name__ == "__main__":
    main()