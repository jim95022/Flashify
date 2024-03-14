from typing import Callable, Any

from django.test import TestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By


def wait(fn: Callable) -> Any:
    max_wait = 10

    def modified_fn(*args, **kwargs) -> Any:
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > max_wait:
                    raise e
                time.sleep(1 / 2)

    return modified_fn


class FunctionalTest(TestCase):

    @wait
    def wait_for(self, fn: Callable) -> Any:
        """Ожидать"""
        return fn()

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=" + ".browser_session")
        cls.browser = WebDriver(options=options)
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.find_element(By.CLASS_NAME, "chat-utils").find_element(By.CLASS_NAME, "btn-menu-toggle").click()
        time.sleep(1)
        cls.browser.find_element(By.XPATH, "//*[contains(text(), 'Block user')]").find_element(By.XPATH, "./..").click()
        time.sleep(1)
        cls.browser.find_element(By.CLASS_NAME, "popup-button").click()
        cls.wait_for(
            lambda: cls.assertIn(
                "start".upper(),
                cls.browser.find_element(By.CLASS_NAME, "chat-input-control").text
            )
        )
        cls.browser.quit()
        super().tearDownClass()

    def test_start_chatbot(self):
        """Test: the beginning work with the chatbot"""

        # User opens telegram bot's chat
        self.browser.get(f"https://web.telegram.org/k/#@jim950022_test_bot")
        self.wait_for(
            lambda: self.assertIn(
                "TestBot",
                self.browser.find_element(By.CLASS_NAME, "chat-info").text
            )
        )

        # He clicks '/start' button and then he sees welcoming message
        self.wait_for(
            lambda: self.assertIn(
                "start".upper(),
                self.browser.find_element(By.CLASS_NAME, "chat-input-control").text
            )
        )
        self.browser.find_element(By.CLASS_NAME, "chat-input-control").click()

        # He tries to input term 'An apple'
        self.browser.find_element(By.CLASS_NAME, "input-message-input").send_keys("An apple")
        self.browser.find_element(By.CLASS_NAME, "input-message-input").send_keys(Keys.ENTER)

        # Bot asks about an inputting of the definition
        self.wait_for(
            lambda: self.assertIn(
                "back card",
                self.browser.find_element(By.CLASS_NAME, "bubbles-group-last").text
            )
        )

        # User inputs the definition 'An apple is a round, edible fruit produced by an apple tree.'
        self.browser.find_element(By.CLASS_NAME, "input-message-input").send_keys("An apple is a round, edible fruit produced by an apple tree.")
        self.browser.find_element(By.CLASS_NAME, "input-message-input").send_keys(Keys.ENTER)

        # Bot accepts the term and the definition.
        #   To verify that everything is correct the bot prints
        #         term
        #       ---------
        #       definition

        # the end
        self.fail("The end of the test")
