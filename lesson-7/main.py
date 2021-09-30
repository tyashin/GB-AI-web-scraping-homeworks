from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import os
import time

if __name__ == "__main__":
    #login = input('Login Mail.ru: ')
    #psswrd = input('Password Mail.ru: ')

    os.name == 'nt'

    driver = webdriver.Chrome(os.path.join(
        os.getcwd(), 'chromedriver.exe' if os.name == 'nt' else 'chromedriver'))
    driver.get("https://light.mail.ru/")

    username = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))

    username.clear()
    username.send_keys(login)
    btn_enter_password = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

    btn_enter_password.click()
    btn_sign_in = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    # без этого хака (попытка входа до ввода пароля) вход не не работает
    btn_sign_in.click()

    password = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name = 'password']")))

    password.clear()
    password.send_keys(psswrd)
    btn_sign_in.click()
    time.sleep(5)
    message_links = driver.find_elements_by_xpath(
        "//a[@class='messageline__link']")

    hrefs = {m.get_attribute('href') for m in message_links}

    for href in hrefs:
