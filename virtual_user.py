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

def register(target, firstname, lastname, email, username, password, gender):
    driver.get(target)
    try:
        driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Create one").click()

        firstname_field = driver.find_element(By.NAME, "firstname")
        firstname_field.clear()
        firstname_field.send_keys(firstname)

        lastname_field = driver.find_element(By.NAME, "lastname")
        lastname_field.clear()
        lastname_field.send_keys(lastname)

        email_field = driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(email)

        username_field = driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys(username)

        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(password)

        password_confirm_field = driver.find_element(By.NAME, "confirmpassword")
        password_confirm_field.clear()
        password_confirm_field.send_keys(password)

        gender_field = driver.find_element(By.CSS_SELECTOR, "input#{genders}".format(genders = gender)).click()

        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(1)

        print("Registration Success")
        return True
    except Exception as e:
        print("Registration failed")
        print(e)
        return False



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

def yourCoach(target, username, password):
    driver.get(target)
    try:
        login(target, username, password)
        driver.find_element(By.LINK_TEXT, "YourCoach").click()
        print("yourCoach Success")
        return True

    except Exception as e:
        print("yourCoach Failed")
        print(e)
        return False

def feedback(target, username, password):
    driver.get(target)
    try:
        login(target, username, password)
        driver.find_element(By.LINK_TEXT, "Feedback").click()
        print("Feedback Success")
        return True

    except Exception as e:
        print("Feedback Failed")
        print(e)
        return False

def profile(target, username, password):
    driver.get(target)
    try:
        login(target, username, password)
        driver.find_element(By.LINK_TEXT, "Profile").click()
        print("Profile Success")
        return True

    except Exception as e:
        print("Profile Failed")
        print(e)
        return False

def assessment(target, username, password):
    driver.get(target)
    try:
        login(target, username, password)
        driver.find_element(By.LINK_TEXT, "Assessment").click()
        print("Assessment Success")
        return True

    except Exception as e:
        print("Assessment Failed")
        print(e)
        return False


def main(target):

    # register(default_target, "virtual_user1", "virtual_user1", "virtual_user@123.com", "virtual_user@123.com", "123456", "male")
    login(default_target, "virtual_user@123.com", "123456")
    logout(default_target)
    

if __name__ == "__main__":
    main(default_target)
