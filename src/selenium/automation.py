from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import os
import random

class TestData:
    def __init__(self, x, y, operator, expected):
        self.x = x
        self.y = y
        self.operator = operator
        self.expected = expected

    def __repr__(self):
        return f"TestData(x={self.x}, y={self.y}, operator={self.operator} expected={self.expected})"

tests = [] # Initialize an array of empty tests
test1 = TestData(5, 4, "+", 9)
tests.append(test1)

test2 = TestData(-5, 4, "-", -9)
tests.append(test2)

test3 = TestData(8, 4, "X", 32)
tests.append(test3)

test4 = TestData(9, 2, "/", 4.5)
tests.append(test4)

test5 = TestData(7, 0, "/", "Can't divide with 0")
tests.append(test5)

# constant values
DEFAULT_DELAY = 0.25
webdriver_path = "chromedriver-mac-x64/chromedriver"

# Start Chrome web browser
service = Service(executable_path=webdriver_path)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

# Open the web page
driver.get("http://localhost:3000")

# Helper function to type in an integer number
# Note: for simplicity, it now only takes single-digit numbers from -9 to 9
def type_in_number(number):
    # click on the number
    button_Number = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[text()='{abs(number)}']")))
    button_Number.click()
    time.sleep(DEFAULT_DELAY)

    if number < 0:
        button_Negative = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='+-']")))
        button_Negative.click()
        time.sleep(DEFAULT_DELAY)

# Run tests
print('DEMO - TEST AUTOMATION WITH SELENIUM')
for test in tests:
    # Reset the calculator
    button_C = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='C']")))
    button_C.click()
    time.sleep(DEFAULT_DELAY)

    # Type in the first number
    type_in_number(test.x)

    # Type in the operator
    operator = test.operator
    xpath = f"//button[normalize-space(text())='{operator}']"
    button_Operator = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    button_Operator.click()
    time.sleep(DEFAULT_DELAY)

    # Type in the second number
    type_in_number(test.y)

    # Click the equal sign to get result
    button_Equal = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='=']")))
    button_Equal.click()
    time.sleep(DEFAULT_DELAY)

    # Check if the result is the same as expected
    result_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.responsive-text")))
    result = result_box.text

    print(f"({test.x}) {test.operator} ({test.y}) = {test.expected}, actual result = {result}.")
    if result == str(test.expected):
        print('PASSED!')
    else:
        print('FAILED!')

# Done
driver.quit()
