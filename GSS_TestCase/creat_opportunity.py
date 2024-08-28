import datetime
import logging
import time

from locators import LocatorActions
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 获取当前时间
now = datetime.datetime.now()
month_day_time = now.strftime("%m%d%H%M%S")

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Chrome 浏览器配置
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-cache')
def initialize_driver():
    try:
        # WebDriver 配置
        webdriver_service = Service(r'E:\Webdriver\chromedriver-win64\chromedriver-win64\chromedriver.exe')
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        logging.info("Chrome 浏览器初始化成功")
        return driver
    except WebDriverException as e:
        logging.error(f"Chrome 浏览器初始化失败: {e}")
        raise

# 登录函数
def login(driver):
    try:
        driver.get(
            'https://cas-server.glodon.com/cas/login?service=https%3A%2F%2Fcas-server.glodon.com%2Fcas%2Fidp%2Fprofile%2FSAML2%2FCallback%3FentityId%3DHTTPS%253A%252F%252Fmy500749-sso.c4c.saphybriscloud.cn')
        time.sleep(2)
        driver.find_element(By.ID, 'username').send_keys('LTC-3')
        driver.find_element(By.ID, 'password').send_keys('Glodon@2023')
        driver.find_element(By.ID, 'SM_BTN_1').click()
        time.sleep(3)
        logging.info("登录成功")
    except NoSuchElementException as e:
        logging.error(f"登录元素未找到: {e}")
        driver.quit()
    except Exception as e:
        logging.error(f"登录过程中出现异常: {e}")
        driver.quit()

# 测试用例1：打开页面并最大化窗口
def test_case1(driver):
    try:
        driver.get(
            'https://my500749-sso.c4c.saphybriscloud.cn/sap/ap/ui/repository/SAP_UI/HTML5/newclient.html?app.component=/SAP_UI_CT/Main/root.uiccwoc&rootWindow=X&redirectUrl=/sap/byd/runtime#Nav/0/eyJfc1dvY0lkIjpudWxsLCJfc1ZpZXdJZCI6bnVsbCwiX3NQZXJmb3JtYW5jZV9zUGVyZm9ybWFuY2VWaWV3SWQiOiJIb21lIiwiX3NDb250ZXh0SWQiOiIyMzJkMTY2Mjk3YTk5MTRjN2UxNGQ0YzA4YTNhODA2MiJ9')
        driver.maximize_window()
        logging.info("页面打开并最大化")
    except Exception as e:
        logging.error(f"测试用例1执行过程中出现异常: {e}")


# 测试用例2：执行一系列操作
def test_case2(driver, locator):
    try:
        locator.wait_and_click("//span[@title='销售']", 100)
        locator.wait_and_click("//a[@title='商机']", 30)

        # 尝试关闭超期提醒
        try:
            overdue_confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[.//bdi[text()="确认"]]'))
            )
            overdue_confirm_button.click()
            logging.info("超期提醒已关闭")
        except TimeoutException:
            logging.info("未检测到超期提醒，继续执行下一步")

        locator.wait_and_click("//span[contains(@data-sap-ui, 'xf')]")
        locator.wait_and_click("//span[@data-sap-automation-id='multiTab-FirstTab-Text2']")
        locator.wait_and_click("//span[@data-sap-automation-id='multiTab-Text2-新建商机']", 100)
        time.sleep(5)

        # 输入商机名称
        logging.info("输入商机名称")
        locator.wait_and_send_keys("//input[contains(@maxlength, '255')]", f"自动化测试商机{month_day_time}")

        # 选择客户
        logging.info("选择客户")
        time.sleep(3)
        locator.wait_and_send_keys('//*[@id="objectvalueselectorHppqevK8aaYFSgcH3xeA1G_348-inputField-inner"]',
                                   "平安喜乐 1000043004")
        driver.find_element(By.XPATH,
                            '//*[@id="objectvalueselectorHppqevK8aaYFSgcH3xeA1G_348-inputField-inner"]').send_keys(
            Keys.ENTER)

        # 点击并选择商机类型
        logging.info("选择商机类型")
        time.sleep(3)
        locator.wait_and_click('//*[@id="dropdownlistbox6db9c5750fd2a06b9d82f9cabfc49b74_352-inner"]')
        time.sleep(3)
        locator.wait_and_click("//li[contains(@class, 'sapMLIB') and .//div[contains(text(), '企业级')]]")
        # 保存企业级商机
        logging.info("保存企业级商机")
        time.sleep(2)
        locator.wait_and_click("//bdi[contains(@id, 'aac')]", 15)


    except TimeoutException as e:
        logging.error(f"元素定位超时: {e}")
        logging.debug(driver.page_source)
    except Exception as e:
        logging.error(f"测试用例2执行过程中出现异常: {e}")

        logging.debug(driver.page_source)
    finally:
        logging.info("测试用例2执行完毕")

# 主函数
def main():
    try:
        # 初始化 WebDriver
        driver = initialize_driver()

        # 初始化定位方法类
        locator = LocatorActions(driver)

        # 执行登录操作
        login(driver)

        # 执行测试用例1
        test_case1(driver)

        # 执行测试用例2
        test_case2(driver, locator)

    except Exception as e:
        logging.error(f"脚本执行过程中出现异常: {e}")
    finally:
        # 关闭浏览器
        time.sleep(5000)
        driver.quit()
        logging.info("浏览器已关闭，测试完成")

if __name__ == "__main__":
    main()
