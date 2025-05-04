from selenium.webdriver.common.by import By
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def by_id(self, value):
        return self.find_element(By.ID, value)

    def by_link_text(self, value):
        return self.find_element(By.LINK_TEXT, value)

    def by_tag_name(self, value):
        return self.find_element(By.TAG_NAME, value)

    def by_xpath(self, value):
        return self.find_element(By.XPATH, value)

    def by_partial_link_text(self, value):
        return self.find_element(By.PARTIAL_LINK_TEXT, value)

    def by_css_selector(self, value):
        return self.find_element(By.CSS_SELECTOR, value)

    def by_class_name(self, value):
        return self.find_element(By.CLASS_NAME, value)

    def by_link(self, value):
        return self.find_element(By.LINK_TEXT, value)


class Type(BasePage):

    def send_keys(self, by, value, keys):
        element = self.find_element(by, value)
        element.send_keys(keys)


class Click(BasePage):
    def click(self, by, value):
        element = self.find_element(by, value)
        element.click()
