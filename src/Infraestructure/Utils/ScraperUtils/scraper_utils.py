from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.chrome.webdriver import WebDriver


def is_xpath_selector_exists(browser: WebDriver, xpath: str) -> bool:
    try:
        browser.find_element_by_xpath(
            xpath
        )
    except (NoSuchElementException, ElementNotVisibleException):
        return False

    return True
