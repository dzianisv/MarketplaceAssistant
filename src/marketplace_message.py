from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def send_message(browser, listing_url, message):
    browser.get(listing_url)

    # Wait until the "Hi, is this available?" textarea is present and send the message.
    textarea = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[contains(text(), 'this available?')]"))
    )
    textarea.clear()  # Clear the default text.
    textarea.send_keys(message)

    # Find the Send button and click it.
    send_button = browser.find_element(By.XPATH, "//span[text()='Send']")
    send_button.click()
