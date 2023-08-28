from seleniumwire import webdriver
from seleniumwire.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

from browser_hz.browser import Browser
from browser_hz.browser_type import BrowserType


def create_browser(browser_type: BrowserType = BrowserType.CHROME) -> Browser:
    match browser_type:
        case BrowserType.CHROME:
            ChromeDriverManager().install()
            options: webdriver.ChromeOptions = webdriver.ChromeOptions()
            driver: Chrome = webdriver.Chrome(options=options)
            driver.maximize_window()
            return Browser(driver)
        case BrowserType.CHROME_HEADLESS:
            ChromeDriverManager().install()
            options: webdriver.ChromeOptions = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver: Chrome = webdriver.Chrome(options=options)
            driver.maximize_window()
            return Browser(driver)
