# locators.py
import logging

import mysql.connector
from mysql.connector import Error
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LocatorActions:
    def __init__(self, driver):
        self.driver = driver

    def wait_and_click(self, xpath, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            ActionChains(self.driver).move_to_element(element).click().perform()
            logging.info(f"元素 '{xpath}' 已点击")
        except TimeoutException as e:
            logging.error(f"等待元素 '{xpath}' 超时: {e}")
            logging.debug(self.driver.page_source)

    def wait_and_send_keys(self, xpath, text, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.clear()
            ActionChains(self.driver).move_to_element(element).click().send_keys(text).perform()
            logging.info(f"已输入 '{text}' 到元素 '{xpath}'")
        except TimeoutException as e:
            logging.error(f"等待元素 '{xpath}' 输入超时: {e}")
            logging.debug(self.driver.page_source)

    def wait_and_click_by_id(self, id, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.ID, id))
            )
            ActionChains(self.driver).move_to_element(element).click().perform()
            logging.info(f"已点击元素 '{id}'")
        except TimeoutException as e:
            logging.error(f"等待元素 '{id}' 超时: {e}")
            logging.debug(self.driver.page_source)

    def wait_and_send_keys_by_id(self, id, text, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.ID, id))
            )
            element.clear()
            ActionChains(self.driver).move_to_element(element).click().send_keys(text).perform()
            logging.info(f"已输入 '{text}' 到元素 '{id}'")
        except TimeoutException as e:
            logging.error(f"等待元素 '{id}' 输入超时: {e}")
            logging.debug(self.driver.page_source)

    def wait_and_send_keys_by_class_name(self, class_name, text, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            )
            ActionChains(self.driver).move_to_element(element).click().send_keys(text).perform()
            logging.info(f"已输入 '{text}' 到元素 '{class_name}'")
        except TimeoutException as e:
            logging.error(f"等待元素 '{class_name}' 输入超时: {e}")
            logging.debug(self.driver.page_source)

    def wait_and_click_class_name(self, class_name, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            )
            ActionChains(self.driver).move_to_element(element).click().perform()
            logging.info(f"已点击元素 '{class_name}'")
        except TimeoutException as e:
            logging.error(f"等待元素 '{class_name}' 超时: {e}")
            logging.debug(self.driver.page_source)


    def wait_and_send_keys_by_css_selector(self, css_selector, text, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )
            ActionChains(self.driver).move_to_element(element).click().send_keys(text).perform()
            logging.info(f"已输入 '{text}' 到元素 '{css_selector}'")
        except TimeoutException as e:
            logging.error(f"等待元素 '{css_selector}' 输入超时: {e}")
            logging.debug(self.driver.page_source)


    def wait_and_click_css_selector(self, css_selector, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )
            ActionChains(self.driver).move_to_element(element).click().perform()
            logging.info(f"已点击元素 '{css_selector}'")
        except TimeoutException as e:
            logging.error(f"等待元素 '{css_selector}' 超时: {e}")
            logging.debug(self.driver.page_source)

    def fetch_data_from_db(self, db_config, query, params):
        """从数据库中获取数据"""
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(query, params)
                result = cursor.fetchone()
                logging.info(f"获取到的数据: {result}")
                return result
        except Error as e:
            logging.error(f"数据库操作错误: {e}")
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

