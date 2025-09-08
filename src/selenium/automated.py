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

# constant values
DEFAULT_DELAY = 0.25
webdriver_path = "chromedriver-mac-x64/chromedriver"
operators = ["+", "-", "X", "/"]
TEST_COUNT = 50 # Number of test cases

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

print('DEMO - AUTOMATED TESTING')
# Run tests
for i in range(0,TEST_COUNT):
    # Reset the calculator
    button_C = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='C']")))
    button_C.click()
    time.sleep(DEFAULT_DELAY)

    # Type in the first number
    x = random.randint(-9,9)
    type_in_number(x)

    operator = random.choice(operators)
    xpath = f"//button[normalize-space(text())='{operator}']"
    button_Operator = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    button_Operator.click()
    time.sleep(DEFAULT_DELAY)

    # Type in the second number
    y = random.randint(-9,9)
    type_in_number(y)

    # Click the equal sign to get result
    button_Equal = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='=']")))
    button_Equal.click()
    time.sleep(DEFAULT_DELAY)

    # Check if the result is the same as expected
    result_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.responsive-text")))
    result = result_box.text

    # Calculate expected result
    expected = ""
    match operator:
        case "+":
            expected = str(x + y)
        case "-":
            expected = str(x - y)
        case "X":
            expected = str(x * y)
        case "/":
            if y != 0:
                tmpResult = x / y
                if tmpResult.is_integer():
                    tmpResult = int(tmpResult)
                expected = str(tmpResult)
            else:
                expected = "Can't divide with 0"
    
    print(f"({x}) {operator} ({y}) = {expected}, actual result = {result}.")
    if result == str(expected):
        print('PASSED!')
    else:
        print('FAILED!')

# Done
driver.quit()
