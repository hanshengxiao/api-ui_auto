
import datetime
import logging
import sys  # 导入 sys 模块以便使用 sys.exit()
import time

import mysql.connector
import requests
from mysql.connector import Error
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from C4_TestCase.test_base.locators import LocatorActions

opportunity_name = "0827184520"
cart_number = 3
opportunity_id = None  # 初始化 opportunity_id 变量

try:
    # 连接到 MySQL 数据库
    conn = mysql.connector.connect(
        host='10.0.106.61',  # 替换为实际的主机地址
        port=8010,  # 如果端口不同于默认值，请指定端口
        user='opportunity',
        password='opportunitytest2024',
        database='opportunity'
    )
    if conn.is_connected():
        cursor = conn.cursor()
        query = "SELECT opportunity_num FROM opportunity.g_opportunity WHERE opportunity_name LIKE %s"
        cursor.execute(query, ('%' + opportunity_name + '%',))
        result = cursor.fetchone()

        if result:
            opportunity_id = result[0]  # 将查询结果的第一个元素赋值给 opportunity_id
            print(f"检索到的 opportunity_id: {opportunity_id}")
        else:
            print("未找到与给定 opportunity_name 匹配的 opportunity_id")

except Error as e:
    print(f"错误: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
# 检查 opportunity_id 是否为空
if opportunity_id is None:
    print("opportunity_id 为空，停止执行")
    sys.exit()  # 停止程序执行

# 如果 opportunity_id 不为空，则继续执行后续代码
print(f"使用 opportunity_id: {opportunity_id}")

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

class WebDriverManager:

    def __init__(self):
        self.driver = None

    @staticmethod
    def initialize_driver():
        try:
            webdriver_service = Service(r'E:\Webdriver\chromedriver-win64\chromedriver-win64\chromedriver.exe')
            driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
            logging.info("Chrome 浏览器初始化成功")
            return driver
        except WebDriverException as e:
            logging.error(f"Chrome 浏览器初始化失败: {e}")
            raise

    @staticmethod
    def close_driver(driver):
        if driver:
            driver.quit()
            logging.info("浏览器已关闭")

class TestAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.locator = LocatorActions(driver)

    def login(self, max_retries=1):
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.driver.get('https://cas-server.glodon.com/cas/login?service=http://zjtest.gyuncai.com/login/sso/glodonLogin')
                self.driver.find_element(By.ID, 'username').send_keys('LTC-3')
                self.driver.find_element(By.ID, 'password').send_keys('Glodon@2023')
                time.sleep(2)
                self.driver.find_element(By.ID, 'SM_BTN_1').click()
                logging.info("登录成功")
                return True  # Login successful, exit the function
            except NoSuchElementException as e:
                logging.error(f"登录元素未找到 (重试 {retry_count + 1}/{max_retries}): {e}")
            except Exception as e:
                logging.error(f"登录过程中出现异常 (重试 {retry_count + 1}/{max_retries}): {e}")

            retry_count += 1
            logging.info(f"正在重试登录... ({retry_count}/{max_retries})")
            time.sleep(3)  # Wait before retrying

        logging.error("登录失败，已达到最大重试次数")
        self.driver.quit()
        return False  # Login failed after max retries

    def test_case1(self):
        try:
            # self.driver.get("https://zjtest.gyuncai.com/mall/mall-view-admin/mallQuotation")
            self.driver.maximize_window()
            logging.info("页面打开并最大化")
            time.sleep(1)
        except Exception as e:
            logging.error(f"测试用例1执行过程中出现异常: {e}")
    def test_case2(self):
        try:
            time.sleep(2)
                    # 从Selenium中获取cookies
            selenium_cookies = self.driver.get_cookies()
            session = requests.Session()
                    # 将Selenium cookies添加到requests会话中
            for cookie in selenium_cookies:
                session.cookies.set(cookie['name'], cookie['value'])


            # 执行POST请求
            url = "https://zjtest.gyuncai.com/material/mallQuotation/insertQuotationFromShopCart"  # 替换为实际的API端点
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "contractInfo": "独立合同",
                "opportunityId": opportunity_id,
                "opportunityName": "自动化测试商机-"+opportunity_name,
                "accountContactName": "宋秀津",
                "cartNum": [
                    #16002732-广联达斑马进度技术服务费
                    {"cartId": 75948,"cartNum": cart_number,"packageList": []},
                    #10000477-12V电源
                    {"cartId": 75947,"cartNum": cart_number,"packageList": []},
                    #10001866-花生壳（物料验收）
                    {"cartId": 75946,"cartNum": cart_number,"packageList": []},
                    #15000078-广联达梦龙物料现场验收管控系统 V3.8
                    {"cartId": 75945,"cartNum": cart_number,"packageList": []},
                    #13000682-GEPS云服务费-20点及以下
                    {"cartId": 75944,"cartNum": cart_number,"packageList": []},
                    #15000145-广联达梦龙施工企业项目管理V9.5（GEPS）-项目信息管理
                    {"cartId": 75943,"cartNum": cart_number,"packageList": []},
                    #16003999-广联达斑马进度计划软件-编辑版-年费制
                    {"cartId": 75942,"cartNum": cart_number,"packageList": []}
                ],
                "sourceType": 4,
                "saleOrgName": "广联达科技股份有限公司",
                "quotationName": "自动化测试合同-"+opportunity_name,
                "c4ClientCode": "1000043004",
                "accountID": "1000043004",
                "accountName": "平安喜乐",
                "sellerEmployeeId": "60000003",
                "sellerEmployeeName": None,
                "sellerEmployeeMobile": None
            }

            print(data)
            # 发起 POST 请求
            try:
                response = session.post(url, json=data, headers=headers)
                print(response)
                print(response.cookies)

                # 检查响应状态码
                if response.status_code == 200:
                    response_data = response.json()
                    order_id = response_data.get('data')

                    if order_id:
                        logging.info(f"POST请求成功: {response_data}")
                        # 使用 order_id 构建新的URL并导航
                        self.driver.get(
                            f"https://zjtest.gyuncai.com/mall/mall-view-admin/quotationDetail/?orderId={order_id}")
                    else:
                        logging.error(f"POST请求成功，但未返回 order_id: {response_data}")
                else:
                    logging.error(f"POST请求失败，状态码: {response.status_code}，响应: {response.text}")

            except requests.exceptions.RequestException as e:
                logging.error(f"POST请求时发生异常: {e}")



            time.sleep(1000)

        except TimeoutException as e:
            logging.error(f"元素定位超时: {e}")
            logging.debug(self.driver.page_source)
        except Exception as e:
            logging.error(f"测试用例2执行过程中出现异常: {e}")
            logging.debug(self.driver.page_source)
        finally:
            logging.info("测试用例2执行完毕")

def main():
    driver = None
    try:
        # 初始化 WebDriver
        driver = WebDriverManager.initialize_driver()
        # 创建自动化测试实例
        test_automation = TestAutomation(driver)
        # 执行登录操作
        test_automation.login()
        # 执行测试用例1
        test_automation.test_case1()
        # 执行测试用例2
        test_automation.test_case2()
    except Exception as e:
        logging.error(f"脚本执行过程中出现异常: {e}")
    finally:
        # 关闭浏览器
        WebDriverManager.close_driver(driver)


if __name__ == "__main__":
    main()

