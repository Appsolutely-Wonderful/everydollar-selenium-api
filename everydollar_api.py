"""
Functions for interacting with the EveryDollar website

pre-requisites:
install geckodriver https://github.com/mozilla/geckodriver/releases
pip install selenium

Credits: This is possible thanks to the developers of selenium and selenium-python
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import time, sleep
from datetime import datetime

class EveryDollarAPI:
    """
    Provides an interface for the everydollar website
    """
    LOGIN_URL = "https://www.everydollar.com/app/sign-in"
    USER_ID_FIELD_ID = "1-email"
    PASSWORD_FIELD_ID = "1-password"
    LOGIN_BTN_XPATH = "//button[.='Sign In']"
    EXPECTED_TITLE_CONTENTS = "Ramsey Account - Sign In"
    ADD_TRANSACTION_MENU_BTN_XPATH = "//button[@data-testid='OperationsPanelTriggerTransactions']"
    ADD_TRANSACTION_BTN_CLASS = "AddTransactionLink-module__AddTransactionLink--f_qUlBKnZh35SSsz"
    ADD_TRANSACTION_BTN_XPATH = "//a[@title='Add Transaction']"
    ADD_NEW_BTN_ID = "TransactionDrawer_addNew"
    AMOUNT_INPUT_CLASS = "TransactionForm-amountInput"
    DATE_INPUT_XPATH = "//input[@name='date']"
    MERCHANT_INPUT_XPATH = "//input[@name='merchant']"
    SELECTOR_TYPE_EXPENSE = "//label[.='Expense']"
    SELECTOR_TYPE_INCOME = "//label[.='Income']"
    TRANSACTION_SUBMIT_BTN_ID = "TransactionModal_submit"
    timeout = 30 # seconds
    def __init__(self):
        """
        Initializes the selenium driver
        """
        opts = Options()
        opts.headless = True
        # opts.binary_location = "/usr/bin/firefox-esr"
        self.driver = webdriver.Firefox(options=opts)

    def close(self):
        """
        Close selenium driver
        """
        self.driver.close()

    def _wait_for_load(self, by, val):
        """
        Waits for the given xpath element to be loaded
        """
        try:
            element_present = EC.presence_of_element_located((by, val))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            raise TimeoutError

    def __del__(self):
        """
        Close selenium driver when object is destroyed
        """
        self.driver.close()

    def login(self, username, password):
        """
        Login to the EveryDollar website by filling in the login
        form with the provided username and password
        """
        self.driver.get(self.LOGIN_URL)
        self._wait_for_load(By.XPATH, self.LOGIN_BTN_XPATH)
        assert self.EXPECTED_TITLE_CONTENTS in self.driver.title
        sleep(2)
        user_field = self.driver.find_element(By.ID, self.USER_ID_FIELD_ID)
        user_field.send_keys(username)
        password_field = self.driver.find_element(By.ID, self.PASSWORD_FIELD_ID)
        password_field.send_keys(password)
        submit_btn = self.driver.find_element(By.XPATH, self.LOGIN_BTN_XPATH)
        submit_btn.click()
        self._wait_for_load(By.XPATH, self.ADD_TRANSACTION_MENU_BTN_XPATH)
        if (self.driver.find_element(By.ID, "Modal_close")):
            self.driver.find_element(By.ID, "Modal_close").click()
        submit_btn = self.driver.find_element(By.XPATH, self.ADD_TRANSACTION_MENU_BTN_XPATH)
        submit_btn.click()
        self._wait_for_load(By.XPATH, self.ADD_TRANSACTION_BTN_XPATH)
        print("Successfully logged in")

    def _open_transaction_menu(self):
        self._wait_for_load(By.XPATH, self.ADD_TRANSACTION_BTN_XPATH)
        self.driver.find_element(By.XPATH, self.ADD_TRANSACTION_BTN_XPATH).click()
        self._wait_for_load(By.XPATH, self.MERCHANT_INPUT_XPATH)

    def _transaction_type(self, type):
        """
        Selects the type of transaction (expense or income)

        input:
            type - string
        """
        if (str.lower(type) == 'expense'):
            self.driver.find_element(By.XPATH, self.SELECTOR_TYPE_EXPENSE).click()
        elif (str.lower(type) == 'income'):
            self.driver.find_element(By.XPATH, self.SELECTOR_TYPE_INCOME).click()
        else:
            print(f"Unexpected transaction type: {type}")

    def _enter_amount(self, amount):
        """
        Enters date into the form.

        input:
            amount - float
        """
        amt_str = str(amount)
        amount_field = self.driver.find_element(By.CLASS_NAME, self.AMOUNT_INPUT_CLASS)
        amount_field.send_keys(amt_str)

    def _enter_date(self, date):
        """
        Enters date into the form.

        input:
            date - datetime object
        """
        date_field = self.driver.find_element(By.XPATH, self.DATE_INPUT_XPATH)
        # Backspace enough to clear the current date
        date_field.send_keys(u'\ue003' * 10)
        # convert datetime to string
        date_str = date.strftime("%m/%d/%y")
        date_field.send_keys(date_str)

    def _enter_merchant(self, merchant):
        """
        Enters the merchant into the form.

        input:
            merchant - string
        """
        merch_input = self.driver.find_element(By.XPATH, self.MERCHANT_INPUT_XPATH)
        merch_input.send_keys(merchant)

    def _submit_transaction(self):
        """
        Submits the add new transaction form
        """
        submit_btn = self.driver.find_element(By.ID, self.TRANSACTION_SUBMIT_BTN_ID)
        submit_btn.click()


    def add_transaction(self, date: datetime , merchant: str, amount: float, type: str = 'expense'):
        self._open_transaction_menu()
        self._transaction_type(type)
        self._enter_amount(amount)
        self._enter_date(date)
        self._enter_merchant(merchant)
        self._submit_transaction()
