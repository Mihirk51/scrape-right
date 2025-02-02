from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def initialize_driver(executable_path: str) -> webdriver.Chrome:
    service = Service(executable_path=executable_path)
    driver = webdriver.Chrome(service=service)
    return driver

def wait_for_element(driver: webdriver.Chrome, by: By, value: str, timeout: int = 10) -> None:
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            driver.find_element(by, value)
            return
        except:
            time.sleep(0.5)
    raise Exception("Element not found within the timeout period.")

def extract_text(element) -> str:
    return element.text.strip() if element else ''

def extract_attribute(element, attribute: str) -> str:
    return element.get_attribute(attribute) if element else ''