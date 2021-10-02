import os
import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    mongobase = client.mail_ru
    collection = mongobase['messages']
    login = input('Login Mail.ru: ')
    psswrd = input('Password Mail.ru: ')
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
    time.sleep(3)
    btn_sign_in = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

    password = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name = 'password']")))

    password.clear()
    password.send_keys(psswrd)
    btn_sign_in.click()
    hrefs = set()

    while True:
        time.sleep(5)
        message_links = driver.find_elements_by_xpath(
            "//a[@class='messageline__link']")

        hrefs.update([m.get_attribute('href') for m in message_links])

        try:
            bttn_nxt = driver.find_element_by_xpath(
                "//a[contains(@class,'paging__item_next')]")

            bttn_nxt.click()
        except:
            break

    for href in hrefs:
        driver.get(href)
        message = {}
        message['text'] = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='viewmessagebody_BODY']"))).text.replace('\u200c', '')

        message['from'] = driver.find_element_by_xpath(
            "//tr[@id='msgFieldFrom']//span[@class='val']").text

        message['date'] = driver.find_element_by_xpath(
            "//div[@class = 'mr_read__date']").text

        message['topic'] = driver.find_element_by_xpath(
            "//div[@id = 'msgFieldSubject']").text

        collection.insert_one(message)

    driver.quit()
