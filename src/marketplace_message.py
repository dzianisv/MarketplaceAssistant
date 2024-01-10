import selenium
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils
import config
from time import sleep
import datetime

logger = config.get_logger(__name__)

def _send_message(browser, listing_url, message):
    browser.get(listing_url)

    try:   
        logger.info("[%s] Waiting for `Message` button load", listing_url)
        element = utils.wait_for(browser, (By.XPATH, "//span[text()='Message Again']"), (By.XPATH, "//span[text()='Message']"))
        if 'Message Again' in element.get_attribute('innerHTML'):
            logger.info("[%s] ✉️ `Message Again` button is located. It means we already sent message to the owner of this ad", listing_url)
            return True
        else:
            ActionChains(browser).move_to_element(element).click().perform()
    except selenium.common.exceptions.TimeoutException:
        logger.warning("[%s] Failed to find `Message` or `Message again` button. Ad is not available?", listing_url)
    
    # type in message
    element = WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((
            By.XPATH, 
            "//span[contains(text(), 'Please type your message to the seller')]/following-sibling::textarea"
    )))
    element.clear()
    element.send_keys(message)
    # ActionChains(browser).scroll_to_element(element).click(element).send_keys(message).perform()

    # click "Send message" button
    element = browser.find_element(By.XPATH, "//span[text()='Send message']") 
    element.click()
    
    # wait for a message delivery
    sleep(10)
    logger.info("[%s] 📤 Message sent", listing_url)

    try:
        browser.find_element(By.XPATH, "//*[contains(text(), 'Something goes wrong')]")
        logger.warning('[%s] Failed to sena a message, "Something goes wrong..."', listing_url)
        return False
    except selenium.common.exceptions.NoSuchElementException:
        pass

    try: 
        browser.find_element(By.XPATH, "//*[contains(text(), 'Your account is restricted right now')]")
        logger.warning('[%s] Failed to sena a message, "Your account is restricted right now"', listing_url)
        return False
    except selenium.common.exceptions.NoSuchElementException:
        pass

    try: 
        browser.find_element(By.XPATH, "//*[contains(text(), \"You've Reached Your Limit\")]")
        logger.warning("[%s] Failed to sena a message, \"You've Reached Your Limit\"", listing_url)
        return False
    except selenium.common.exceptions.NoSuchElementException:
        pass
    

    return True

def send_message(browser, listing_url, message):
    try:
        return _send_message(browser, listing_url, message)
    except selenium.common.exceptions.MoveTargetOutOfBoundsException as e:
        logger.warning("[%s] Failed to send message because controls are not available (MoveTargetOutOfBoundsExceptio): %s", listing_url, e)
        return True