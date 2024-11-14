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

    def _wait_for_element(self, locator_type, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((locator_type, locator))
            )
            return element
        except TimeoutException as e:
            logging.error(f"等待元素 '{locator}' 超时: {e}")
            logging.debug(self.driver.page_source)
            return None

    def _perform_action(self, element, action, *args):
        if element:
            action_chains = ActionChains(self.driver)
            action(action_chains, element, *args).perform()
        else:
            logging.error("未找到要操作的元素")

    def wait_and_click(self, xpath, timeout=10):
        element = self._wait_for_element(By.XPATH, xpath, timeout)
        self._perform_action(element, lambda ac, el: ac.move_to_element(el).click())

    def wait_and_send_keys(self, xpath, text, timeout=10):
        element = self._wait_for_element(By.XPATH, xpath, timeout)
        if element:
            element.clear()
            self._perform_action(element, lambda ac, el: ac.move_to_element(el).click().send_keys(text))
            logging.info(f"已输入 '{text}' 到元素 '{xpath}'")

    def wait_and_click_by_id(self, id, timeout=10):
        self.wait_and_click(By.ID, id, timeout)

    def wait_and_send_keys_by_id(self, id, text, timeout=10):
        self.wait_and_send_keys(By.ID, id, text, timeout)

    def wait_and_click_class_name(self, class_name, timeout=10):
        self.wait_and_click(By.CLASS_NAME, class_name, timeout)

    def wait_and_send_keys_by_class_name(self, class_name, text, timeout=10):
        self.wait_and_send_keys(By.CLASS_NAME, class_name, text, timeout)

    def wait_and_click_css_selector(self, css_selector, timeout=10):
        self.wait_and_click(By.CSS_SELECTOR, css_selector, timeout)

    def wait_and_send_keys_by_css_selector(self, css_selector, text, timeout=10):
        self.wait_and_send_keys(By.CSS_SELECTOR, css_selector, text, timeout)

    def fetch_data_from_db(self, db_config, query, params):
        """从数据库中获取数据"""
        try:
            with mysql.connector.connect(**db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchone()
                    logging.info(f"获取到的数据: {result}")
                    return result
        except Error as e:
            logging.error(f"数据库操作错误: {e}")
            return None

    def assert_element_title(self, xpath, expected_title):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            title_value = element.get_attribute('title')
            assert title_value == expected_title, f"断言失败: 期望 title 是 {expected_title}，但实际是 {title_value}"
            logging.info(f"断言成功: title == {expected_title}")
        except AssertionError as e:
            logging.error(f"断言错误: {e}")
        except Exception as e:
            logging.error(f"断言时发生异常: {e}")
