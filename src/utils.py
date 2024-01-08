from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os

COOKIES_FILE="fbAssistantCookies.pkl"

def waitFor(browser, selector, timeout_s=30):
    return WebDriverWait(browser, 30).until(
        EC.presence_of_element_located(selector)
    )

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