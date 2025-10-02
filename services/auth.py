from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from config import USER, PASSWORD, URL_INICIAL, URL_LOGOUT

def iniciar_driver(headless=True):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    if headless:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login(driver):
    driver.get(URL_INICIAL)
    time.sleep(2)

    user_field = driver.find_element(By.ID, "fieldUser")
    pass_field = driver.find_element(By.ID, "fieldPassword")

    user_field.send_keys(USER)
    pass_field.send_keys(PASSWORD)
    pass_field.send_keys(Keys.RETURN)
    time.sleep(5)

    if "processoView.elaw" in driver.current_url or "homePage.elaw" in driver.current_url:
        return True
    return False

def logout(driver):
    driver.get(URL_LOGOUT)
    time.sleep(2)
