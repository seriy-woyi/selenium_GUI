import time

from selenium import webdriver
from selenium.webdriver.common.by import By
driver=webdriver.Edge()
driver.get("https://baidu.com")
driver.find_element(By.ID,'kw').send_keys("lllll")
time.sleep(5)
driver.find_element(By.ID,"su").click()
time.sleep(6)
