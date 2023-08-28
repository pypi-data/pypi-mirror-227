from selenium.webdriver.chrome.service import Service as ChromeService
from seleniumwire import webdriver
from seleniumwire.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

from browser.browser import Browser
from browser.browser_type import BrowserType


def create_browser(browser_type: BrowserType = BrowserType.CHROME) -> Browser:
    match browser_type:
        case BrowserType.CHROME:
            driver: Chrome = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install())
            )
            driver.maximize_window()
            return Browser(driver)
