#!/usr/bin/env python3

import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from listings import find_listings
from marketplace_message import send_message
import utils
import pickle
import config
import random
import enum
import hashlib
import argparse
from llm import LLM

logger = config.get_logger(__name__)


def llm_improve_message(message):
    messages = [
        {
            "role": "system",
            "content": f"You are professional socia media marketer and writer",
        },
        {"role": "user", "content": message},
    ]

    # chatgpt insers ``` as in the original message, ignore it`
    response = LLM().get_response(messages).replace("```", "")
    return response


def get_messages(args):
    if args.llm_message:
        with open(args.llm_message, "r", encoding="utf8") as f:
            query = f.read()

        while True:
            yield llm_improve_message(query)
    else:
        with open(args.messages, "r", encoding="utf8") as f:
            messages = f.read().split("---\n")

        while True:
            yield random.choice(messages)

def login_to_facebook(browser, email, password):
    browser.get("https://www.facebook.com/")
    try:
        # Input email
        email_element = browser.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_element.send_keys(email)

        # Input password
        password_element = browser.find_element(By.CSS_SELECTOR, 'input[name="pass"]')
        password_element.send_keys(password)
        password_element.send_keys(Keys.ENTER)
    except selenium.common.exceptions.NoSuchElementException:
        logger.info(
            "`email` and `pass` fields are not found, looks like we are logged in..."
        )

    logger.debug("waiting for `Marketplace` menu item")
    utils.wait_for(browser, (By.XPATH, "//span[text()='Marketplace']"))


class Browsers(enum.Enum):
    FIREFOX = 0
    CHROME = 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--listings",
        default=None,
        type=str,
        help="path to the listings file. Listings file contains url of ad listings that will be used",
    )
    parser.add_argument(
        "--enable-cache", action="store_true", help="enable listing caching"
    )
    parser.add_argument(
        "--llm-message",
        type=str,
        help="use the LLM (gpt-3.5) to generate a unique message",
    )
    parser.add_argument(
        "--messages",
        type=str,
        default="messages.txt",
        help="use a text file with messages separated by ---\\n",
    )

    args = parser.parse_args()

    # Initialize the browse
    browser_type = Browsers.CHROME

    m = hashlib.sha1()
    m.update(config.EMAIL.encode("utf-8"))
    profile_path = ".profile." + m.hexdigest() + "." + browser_type.name

    if browser_type == Browsers.FIREFOX:
        options = selenium.webdriver.firefox.options.Options()
        options.add_argument("--profile")
        options.add_argument(profile_path)
        browser = webdriver.Firefox(options=options)
    else:
        options = selenium.webdriver.chrome.options.Options()
        options.add_argument("--user-data-dir=" + profile_path)
        browser = webdriver.Chrome(options=options)

    find_and_message(browser, args)


def test(browser):
    send_message(
        browser,
        "https://www.facebook.com/marketplace/item/1049990203002744/?ref=category_feed&referral_code=undefined&referral_story_type=listing&tracking=%7B%22qid%22%3A%22-2753636296707797484%22%2C%22mf_story_key%22%3A%226998066960287720%22%2C%22commerce_rank_obj%22%3A%22%7B%5C%22target_id%5C%22%3A6998066960287720%2C%5C%22target_type%5C%22%3A0%2C%5C%22primary_position%5C%22%3A28%2C%5C%22ranking_signature%5C%22%3A7594008407766888175%2C%5C%22commerce_channel%5C%22%3A504%2C%5C%22value%5C%22%3A4.9311299286001e-5%2C%5C%22candidate_retrieval_source_map%5C%22%3A%7B%5C%226998066960287720%5C%22%3A204%7D%7D%22%2C%22ftmd_400706%22%3A%22111112l%22%7D",
        random.choice(config.MESSAGES),
    )


def find_and_message(browser, args):
    try:
        # Login to Facebook
        login_to_facebook(browser, config.EMAIL, config.PASSWORD)

        # Parameters for searching and messaging
        # seattle, miami, sanjuan
        prices = (800, 1500)
        if args.listings:
            with open(args.listings, "r", encoding="utf8") as f:
                logger.info("reading URLs from %s", args.listings)
                listings = f.read().splitlines()
        elif args.enable_cache and os.path.exists("listings.cache.pkl"):
            listings = pickle.load(open("listings.cache.pkl", "rb"))
        else:
            listings = find_listings(browser, prices, "")
            pickle.dump(listings, open("listings.cache.pkl", "wb"))

        messages = get_messages(args)

        timeouts = 0
        for i in range(len(listings)):
            if i > config.MESSAGES_LIMIT:
                logger.info("messages quota is reached")
                break

            listing = listings[i]

            for retry_i in range(3):
                try:
                    if not send_message(browser, listing, next(messages)):
                        logger.error("Failed to send a message")
                        return False
                    break  # end retries loop
                except selenium.common.exceptions.TimeoutException:
                    timeouts += 1
                    logger.error("timed out on %s", listing)
                    continue
            # dump current state to start from a failed one next time
            pickle.dump(listings[i:], open("listings.cache.pkl", "wb"))

        os.unlink("listings.cache.pkl")
        logger.info("Done, timeouts: %d", timeouts)
    finally:
        # Quit the browser after completing the tasks
        # browser.quit()
        pass


if __name__ == "__main__":
    main()
