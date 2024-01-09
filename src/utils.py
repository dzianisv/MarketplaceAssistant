from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
import pickle
import os

COOKIES_FILE="fbAssistantCookies.pkl"

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

def save_cookies(driver):
    with open(COOKIES_FILE, "wb") as fd:
        pickle.dump(driver.get_cookies(), fd)

def load_coockies(driver):
    if not os.path.exists(COOKIES_FILE):
        return False

    with open(COOKIES_FILE, "rb") as fd:
        cookies = pickle.load(fd)
        for cookie in cookies:
            driver.add_cookie(cookie)
            return True

def waitPageReady(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

def wait(driver, timeout=10):
    driver.implicitly_wait(timeout)

def scrollToBottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")