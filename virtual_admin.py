import requests
import time
import getpass
import selenium
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

s = Service("webdriver/chromedriver")
default_target = "http://43.129.230.213/"
driver = webdriver.Chrome(service=s)

def login(target, username, password):
    driver.get(target)
    try:
        driver.find_element(By.LINK_TEXT, "Login").click()

        username_field = driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys(username)

        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(password)

        driver.find_element(By.XPATH, "//input[@type='submit']").click()

        print("Login Success")
        return True
    except Exception as e:
        print("Login Failed")
        print(e)
        return False


def logout(target):
    driver.get(target)
    try:
        driver.find_element(By.LINK_TEXT, "Logout").click()
        print("Logout Success")
        return True
    except Exception as e:
        print("Logout Failed")
        print(e)
        return False


def main(target):
    login(default_target, "admin", "admin")
    logout(default_target)

if __name__ == "__main__":
    main(default_target)
