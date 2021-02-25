from selenium.webdriver.chrome.webdriver import WebDriver

from src.Infraestructure.Utils.ScraperUtils.scraper_utils import is_xpath_selector_exists


class Download:
    def __init__(self, browser: WebDriver):
        self._browser = browser

    def download(self, url: str):
        self._browser.get(url)

        while not is_xpath_selector_exists(self._browser, "//div[@id='notice']"):
            pass

