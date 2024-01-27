from django.test import TestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class FunctionalTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_start_chatbot(self):
        """Test: the beginning work with the chatbot"""

        # User opens telegram bot's chat
        self.selenium.get(f"https://web.telegram.org/k/#@jim950022_test_bot")
        self.fail("The end of the test")
        # He clicks '/start' button and then he sees welcoming message

        # He tries to input term 'An apple'

        # Bot asks about an inputting of the definition 'An apple is a round, edible fruit produced by an apple tree.'

        # User inputs the definition

        # Bot accepts the term and the definition.
        #   To verify that everything is correct the bot prints
        #         term
        #       ---------
        #       definition

        # the end
