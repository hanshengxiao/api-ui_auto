import datetime
import logging
import random
import time

import mysql

from GSS_TestCase.base.locators import LocatorActions
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from mysql.connector import Error



plan_monney=round(random.uniform(0.001, 0.05), 3)
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
# 添加断言函数

# 登录函数
def login(driver, locator):
    try:
        driver.get(
            'https://cas-server.glodon.com/cas/login?service=http%3A%2F%2Fgss-test.glodon.com%2Fweb%2F')
        time.sleep(2)
        driver.find_element(By.ID, 'username').send_keys('')
        driver.find_element(By.ID, 'password').send_keys('')
        driver.find_element(By.ID, 'SM_BTN_1').click()
        time.sleep(3)
        logging.info("登录成功")

        # 点击销售计划，点击销售计划子菜单
        locator.wait_and_click('//*[@id="app"]/section/section/aside/div[1]/div[2]/div[1]/div/ul/li[2]/div', 100)
        locator.wait_and_click('//*[@id="app"]/section/section/aside/div[1]/div[2]/div[1]/div/ul/li[2]/ul/li/span', 30)

    except NoSuchElementException as e:
        logging.error(f"登录元素未找到: {e}")
        driver.quit()
    except Exception as e:
        logging.error(f"登录过程中出现异常: {e}")
        driver.quit()


# 测试用例1：测试未移交合同盘点
def test_case1(driver, locator):
    try:

        #搜索编号
        locator.wait_and_send_keys('//*[@id="form_item_contractNum"]', '5000023357')
        time.sleep(1)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[2]/span',100)
        time.sleep(3)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[1]/span', 100)



        #搜索名称
        locator.wait_and_send_keys('//*[@id="form_item_contractName"]', '售前申请业绩划分测试')
        time.sleep(1)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[2]/span', 100)
        time.sleep(3)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[1]/span', 100)





        # # 搜索计划交底日期
        # # 定位日期输入框并直接输入日期
        # start_date_input = driver.find_element(By.ID,'form_item_plannedDisclosureDate')
        # start_date_input.clear()  # 清除之前的值
        # start_date_input.send_keys('2024-09-01')
        # time.sleep(1)
        # # 同样处理结束日期
        # end_date_input = driver.find_element(By.XPATH,'//input[@placeholder="结束日期"]')
        # end_date_input.clear()
        # end_date_input.send_keys('2024-10-16')
        # locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[2]/span', 100)
        # time.sleep(3)
        # locator.wait_and_click(
        #     '//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[1]/span',
        #     100)


        # 搜索合同主售产品
        time.sleep(3)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[4]/div/div/div[2]/div/div/div/div/div/div/span',5)
        time.sleep(1)
        locator.wait_and_click( '//*[@id="161"]/div',5)
        time.sleep(1)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div', 5)
        time.sleep(1)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[2]/span',100)
        time.sleep(3)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[1]/span',100)


        #搜索编号
        locator.wait_and_send_keys('//*[@id="form_item_sell"]', '销售')
        time.sleep(1)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[2]/span',100)
        time.sleep(3)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/form/div/div[6]/div/div/div/div/div/div/button[1]/span', 100)

        # 加入断言
        # assert_element_text(driver, '//*[@id="contractName_result_xpath"]', '售前申请业绩划分测试')

        time.sleep(2)



    except TimeoutException as e:
        logging.error(f"元素定位超时: {e}")
        logging.debug(driver.page_source)
    except Exception as e:
        logging.error(f"测试用例2执行过程中出现异常: {e}")

        logging.debug(driver.page_source)
    finally:
        logging.info("测试用例2执行完毕")


def test_case2(driver, locator):
    try:
        # 假设有其他测试步骤和断言
        logging.info("测试用例2开始执行")

        time.sleep(3)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/div/div/div/div/div[1]/div/div[1]/div[1]/div/span[2]',2)
        time.sleep(1)
        locator.wait_and_click_css_selector("div[title='未盘点合同'] div[class='ant-select-item-option-content']",2)
        # 搜索编辑
        time.sleep(2)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/div/div/div/div/div[2]/div[2]/table/tbody/tr[2]/td[1]/label',2)
        time.sleep(1)
        locator.wait_and_click('//*[@id="app"]/section/section/section/div[3]/div/div[2]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div[1]/button[2]/span',2)
        time.sleep(1)
        locator.wait_and_send_keys('//*[@id="form_item_plannedAmount"]',plan_monney)
        time.sleep(1)
        locator.wait_and_click("//button[@class='css-q7pu1z ant-btn ant-btn-primary']",2)
        time.sleep(3)






        #批量编辑

    except Exception as e:
        logging.error(f"测试用例2执行过程中出现异常: {e}")
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
        login(driver, locator)

        # 执行测试用例1
        # test_case1(driver, locator)
        # 执行测试用例1
        test_case2(driver, locator)

    except Exception as e:
        logging.error(f"脚本执行过程中出现异常: {e}")
    finally:
        # 关闭浏览器
        time.sleep(5)
        driver.quit()
        logging.info("浏览器已关闭，测试完成")

if __name__ == "__main__":
    main()
