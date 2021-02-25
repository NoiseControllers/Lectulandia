import time
import os

import pyperclip
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.webdriver import WebDriver

from src.Infraestructure.Utils.ScraperUtils.scraper_utils import is_xpath_selector_exists


class SandUpCo:
    def __init__(self, webdriver: WebDriver):
        self._browser = webdriver
        self._base_url = 'http://sandup.co/?op=upload_form'

    def upload_file(self, file_name: str):
        self._browser.get(self._base_url)
        time.sleep(5)

        self._browser.find_element_by_xpath("//input[@id='file_0']").send_keys(f'{os.getcwd()}\\temp\\{file_name}')
        time.sleep(2)

        if is_xpath_selector_exists(self._browser, f"//h4[contains(text(),'{file_name}')]"):
            print('[DEBUG] Archivo subido correctamente.')
            # Button Start upload form
            self._browser.execute_script('document.querySelector("#upload_controls > input.btn.btn-primary").click()')

            while True:
                time.sleep(0.5)
                if is_xpath_selector_exists(self._browser, "//button[contains(text(), 'Copy')]"):
                    try:
                        self._browser.find_element_by_xpath("//button[contains(text(), 'Copy')]").click()
                        link = pyperclip.paste()
                        return link
                    except ElementNotInteractableException:
                        pass
