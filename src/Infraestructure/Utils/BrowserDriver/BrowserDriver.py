from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class BrowserDriver:
    def init(self) -> WebDriver:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('log-level=3')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-infobars')
        # chrome_options.add_argument('--headless')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        return webdriver.Chrome(options=chrome_options)
