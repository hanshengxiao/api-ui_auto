# -*- coding: utf-8 -*-
import json
import logging
import sys
import time

import mysql.connector
import requests
from mysql.connector import Error
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestAutomation:
    def __init__(self):
        self.order_id = None
        self.opportunity_name = "0828-1721"
        self.cart_number = 2
        self.opportunity_id = None
        self.driver = None
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument('--disable-cache')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    def connect_to_database(self):
        try:
            conn = mysql.connector.connect(
                host='10.0.106.61',
                port=8010,
                user='opportunity',
                password='opportunitytest2024',
                database='opportunity'
            )
            if conn.is_connected():
                cursor = conn.cursor()
                query = "SELECT opportunity_num FROM opportunity.g_opportunity WHERE opportunity_name LIKE %s"
                cursor.execute(query, ('%' + self.opportunity_name + '%',))
                result = cursor.fetchone()
                self.opportunity_id = result[0] if result else None
                if self.opportunity_id:
                    logging.info(f"检索到的 opportunity_id: {self.opportunity_id}")
                else:
                    logging.error("未找到与给定 opportunity_name 匹配的 opportunity_id")
        except Error as e:
            logging.error(f"数据库连接错误: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        if not self.opportunity_id:
            logging.error("opportunity_id 为空，停止执行")
            sys.exit()
    def initialize_driver(self):
        try:
            webdriver_service = Service(r'E:\Webdriver\chromedriver-win64\chromedriver-win64\chromedriver.exe')
            self.driver = webdriver.Chrome(service=webdriver_service, options=self.chrome_options)
            logging.info("Chrome 浏览器初始化成功")
        except WebDriverException as e:
            logging.error(f"Chrome 浏览器初始化失败: {e}")
            raise
    def close_driver(self):
        if self.driver:
            self.driver.quit()
            logging.info("浏览器已关闭")
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
                return True
            except NoSuchElementException as e:
                logging.error(f"登录元素未找到 (重试 {retry_count + 1}/{max_retries}): {e}")
            except Exception as e:
                logging.error(f"登录过程中出现异常 (重试 {retry_count + 1}/{max_retries}): {e}")

            retry_count += 1
            logging.info(f"正在重试登录... ({retry_count}/{max_retries})")
            time.sleep(3)

        logging.error("登录失败，已达到最大重试次数")
        self.close_driver()
        return False
    def execute_test_cases(self):
        try:
            try:# self.driver.get("https://zjtest.gyuncai.com/mall/mall-view-admin/mallQuotation")
                self.driver.maximize_window()
                logging.info("页面打开并最大化")
                time.sleep(5)
            except Exception as e:
               logging.error(f"测试用例1执行过程中出现异常: {e}")

            # 从Selenium中获取cookies
            logging.info("正在获取cookies...")
            time.sleep(2)
            selenium_cookies = self.driver.get_cookies()
            session = requests.Session()
            for cookie in selenium_cookies:
                session.cookies.set(cookie['name'], cookie['value'])

            url = "https://zjtest.gyuncai.com/material/mallQuotation/insertQuotationFromShopCart"
            headers = {
                "Content-Type": "application/json"
            }
            data =  {
                "contractInfo": "独立合同",
                "opportunityId": self.opportunity_id,
                "opportunityName": "自动化测试企业级商机-"+self.opportunity_name,
                "accountContactName": "宋秀津",
                "cartNum": [
                    #16002732-广联达斑马进度技术服务费
                    {"cartId": 75948,"cartNum": self.cart_number,"packageList": []},
                    #10000477-12V电源
                    {"cartId": 75947,"cartNum": self.cart_number,"packageList": []},
                    #10001866-花生壳（物料验收）
                    {"cartId": 75946,"cartNum": self.cart_number,"packageList": []},
                    #15000078-广联达梦龙物料现场验收管控系统 V3.8
                    {"cartId": 75945,"cartNum": self.cart_number,"packageList": []},
                    #13000682-GEPS云服务费-20点及以下
                    {"cartId": 75944,"cartNum": self.cart_number,"packageList": []},
                    #15000145-广联达梦龙施工企业项目管理V9.5（GEPS）-项目信息管理
                    {"cartId": 75943,"cartNum": self.cart_number,"packageList": []},
                    # 16003999-广联达斑马进度计划软件-编辑版-年费制
                    {"cartId": 75942,"cartNum": self.cart_number,"packageList": []}
                ],
                "sourceType": 4,
                "saleOrgName": "广联达科技股份有限公司",
                "quotationName": "自动化测试企业级合同-"+self.opportunity_name,
                "c4ClientCode": "1000043004",
                "accountID": "1000043004",
                "accountName": "平安喜乐",
                "sellerEmployeeId": "60000003",
                "sellerEmployeeName": None,
                "sellerEmployeeMobile": None
            }
            json_data = json.dumps(data, ensure_ascii=False, indent=4)
            print(json_data)
            response = session.post(url, json=data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                order_id = response_data.get('data')
                if order_id:
                    logging.info(f"POST请求成功: {response_data}")
                    self.driver.get(
                        f"https://zjtest.gyuncai.com/mall/mall-view-admin/quotationDetail/?orderId={order_id}")
                    self.order_id = order_id
                else:
                    logging.error(f"POST请求成功，但未返回 order_id: {response_data}")
            else:
                logging.error(f"POST请求失败，状态码: {response.status_code}，响应: {response.text}")

            # File upload
            url_upload = "https://zjtest.gyuncai.com/base/upload/uploadFileToObs?type=estimate"
            files = [
                ('file', (
                    '项目概算利润表导入模板 (2).xlsx',
                    open(r'C:\Users\tiezh\Downloads\项目概算利润表导入模板 (2).xlsx', 'rb'),
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
            ]
            headers_upload = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'origin': 'https://zjtest.gyuncai.com',
                'personalflag': 'enterprise',
                'priority': 'u=1, i',
                'referer': f'https://zjtest.gyuncai.com/mall/mall-view-admin/quotationDetail/?orderId={self.order_id}',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
                'x-requested-with': 'XMLHttpRequest',
                'x-top-window': 'true'
            }
            response_upload = session.post(url_upload, headers=headers_upload, files=files)
            logging.info(f"文件上传响应: {response_upload.text}")

            # Estimate upload
            url_estimate = "https://zjtest.gyuncai.com/api/material/customer/estimate/uploadEstimate"
            payload_estimate = {
                "quotationId": str(self.order_id),
                "fileUrl": "test/estimate/f1343b1244dd46bc8624e3b236f1e048.xlsx",
                "fileName": "项目概算利润表导入模板 (2).xlsx",
                "jobNumber": ""
            }
            headers_estimate = {
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://zjtest.gyuncai.com',
                'personalflag': 'enterprise',
                'priority': 'u=1, i',
                'referer': f'https://zjtest.gyuncai.com/mall/mall-view-admin/quotationDetail/?orderId={self.order_id}',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
                'x-requested-with': 'XMLHttpRequest',
                'x-top-window': 'true'
            }
            response_estimate = session.post(url_estimate, headers=headers_estimate, json=payload_estimate)
            logging.info(f"上传估算响应: {response_estimate.text}")

        except TimeoutException as e:
            logging.error(f"元素定位超时: {e}")
            logging.debug(self.driver.page_source)
        except Exception as e:
            logging.error(f"测试用例执行过程中出现异常: {e}")
            logging.debug(self.driver.page_source)
        finally:
            logging.info("测试用例执行完毕")
    def test_case2(self):
        time.sleep(5)
        logging.info("测试用例2开始执行")
        self.driver.find_element(By.XPATH,'//*[@id="app-main"]/div/div[2]/div[1]/div[1]/form/div[6]/div/label/span[1]/span').click()
        time.sleep(3)
        logging.info("测试用例2开始执行提交")
        self.driver.find_element(By.XPATH,'//*[@id="app-main"]/div/div[2]/div[1]/div[2]/div/button[1]/span').click()
        time.sleep(3)
        self.driver.find_element(By.XPATH,'//*[@id ="app-main"]/div/div[2]/div[1]/div[3]/div[3]/div/div[3]/span/button[2]').click()
        # 尝试关闭超期提醒
        time.sleep(3)
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[5]/div/div[3]/button[2]/span').click()
            logging.info("报价单包含非固定成本价物料，请您注意核对物料成本价提醒已关闭")
        except TimeoutException:
            logging.info("未检测到提醒，继续执行下一步")



        time.sleep(10)
        self.driver.refresh()
        time.sleep(5)
        self.driver.refresh()
        time.sleep(5)
        self.driver.refresh()
        time.sleep(5)
        self.driver.refresh()
        time.sleep(5)
        self.driver.refresh()
        time.sleep(5)
        self.driver.refresh()

        # 等待元素出现
        wait = WebDriverWait(self.driver, 1000)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pane-productList"]/div[1]/div/div[1]/div/span/p[1]')))
        # 断言元素文本
        assert element.text == "合同已生成", f"期望的文本是 '合同已生成'，但实际找到的是 '{element.text}'"

        logging.info("测试用例2执行完毕")


        # 设置日志记录器
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        # 初始化倒计时的秒数
        seconds_left = 30
        # 开始倒计时
        while seconds_left > 0:
            logging.info(f"剩余时间: {seconds_left}秒")
            time.sleep(1)  # 暂停1秒
            seconds_left -= 1
        logging.info("倒计时结束")
        # 关闭浏览器
        self.driver.quit()
    def run(self):
        try:
            self.connect_to_database()
            self.initialize_driver()
            if self.login():
                self.execute_test_cases()
                self.test_case2()
        except Exception as e:
            logging.error(f"脚本执行过程中出现异常: {e}")
        finally:
            self.close_driver()

if __name__ == "__main__":
    automation = TestAutomation()
    automation.run()
# -*- coding: utf-8 -*-