from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
import pickle
import os

def wait_for(browser, *args):
    def _f(driver):
        for selector in args:
            try:
                element = driver.find_element(*selector)
                return element
            except selenium.common.exceptions.NoSuchElementException:
                pass
        return None

    return WebDriverWait(browser, 30).until(_f)

def wait(driver, timeout=10):
    driver.implicitly_wait(timeout)

def scrollToBottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")