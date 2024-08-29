import datetime
import logging
import time

from C4_TestCase.test_base.locators import LocatorActions
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
month_day_time = now.strftime("%m%d-%H%M")

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Chrome 浏览器配置s
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
        locator.wait_and_send_keys("//input[contains(@maxlength, '255')]", f"自动化测试企业级商机{month_day_time}")

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

        # 选择联系人
        logging.info("选择联系人")
        time.sleep(2)
        locator.wait_and_send_keys('//*[@id="objectvalueselectorDJFL3kMLhK_OJoDgE62YbW_360-inputField-inner"]',
                                   "宋秀津")
        driver.find_element(By.XPATH,
                            '//*[@id="objectvalueselectorDJFL3kMLhK_OJoDgE62YbW_360-inputField-inner"]').send_keys(
            Keys.ENTER)

        # 选择联系人角色
        logging.info("选择联系人角色")
        time.sleep(3)
        locator.wait_and_send_keys_by_id('dropdownlistbox7c095e0122254f5bbe23443c743896d6_384-inner', "使用人")
        locator.wait_and_click_by_id('__item230-content', 30)

        # 点击并选择来源
        logging.info("选择来源")
        time.sleep(3)
        locator.wait_and_click_by_id('dropdownlistboxmyokgu9MOqQ2YL10sdWYN0_364-arrow', 30)
        time.sleep(3)
        locator.wait_and_click("//li[contains(@class, 'sapMLIB') and .//div[contains(text(), '客户拜访')]]")

        # 点击并选择对计划的态度
        logging.info("选择对计划的态度")
        time.sleep(3)
        locator.wait_and_click_by_id('dropdownlistboxbf8d813660b080d12db0ee642ab52970_388-arrow', 30)
        time.sleep(3)
        locator.wait_and_click("//li[contains(@class, 'sapMLIB') and .//div[contains(text(), '支持')]]")

        # 点击并选择实际购买层级
        logging.info("选择实际购买层级")
        time.sleep(3)
        locator.wait_and_click_by_id('dropdownlistbox1824dff254b1e84c03f67f7a307bdd6c_408-arrow', 30)
        time.sleep(3)
        locator.wait_and_click("//li[contains(@class, 'sapMLIB') and .//div[contains(text(), '集团公司/局公司')]]")

        # 点击并选择是否有规划
        logging.info("选择是否有规划")
        time.sleep(3)
        locator.wait_and_click_by_id('dropdownlistbox7d9a4f7280a67b7d935aa644bfa342bd_623-arrow', 30)
        time.sleep(3)
        locator.wait_and_click("//li[contains(@class, 'sapMLIB') and .//div[contains(text(), '是')]]")

        # 点击并选择是否有负责人
        logging.info("选择是否有负责人")
        time.sleep(3)
        locator.wait_and_send_keys_by_id('dropdownlistboxc48f243ef19ff574ce8ea8648732b880_627-inner', "是")


        # 点击并选择是否有需求
        logging.info("选择是否有需求")
        time.sleep(3)
        locator.wait_and_send_keys_by_id('dropdownlistboxfa17bfb6e2a94344dbe4dbbb8f889df4_631-inner', "是")


        # 点击并选择是否有预算
        logging.info("选择是否有预算")
        time.sleep(3)
        locator.wait_and_send_keys_by_id('dropdownlistbox4ea225a267c5a45982364c556b6d9072_635-inner', "是")
        time.sleep(3)
        driver.find_element(By.ID,
                            'dropdownlistbox4ea225a267c5a45982364c556b6d9072_635-inner').send_keys(
            Keys.ENTER)


        # 添加产品--企业级
        logging.info("添加产品--企业级")
        time.sleep(3)
        locator.wait_and_click_by_id('button3vks4Vj2c4Y2G2O3ss9AM0_962-inner', 15)
        time.sleep(4)
        locator.wait_and_click("//span[contains(@data-sap-ui, 'objectvalueselectorh')]", 15)
        time.sleep(3)
        locator.wait_and_click("//span[@title='其他']", 15)
        time.sleep(1)
        locator.wait_and_send_keys("//input[@value='0.00']", "43000")

        # 保存企业级商机

        time.sleep(15)
        logging.info("保存企业级商机")
        locator.wait_and_click("//bdi[contains(@id, 'aac')]", 15)

        print(month_day_time)



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
        print("自动化测试商机"+month_day_time)

    except Exception as e:
        logging.error(f"脚本执行过程中出现异常: {e}")
    finally:
        # 设置日志记录器
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        # 初始化倒计时的秒数
        seconds_left = 20
        # 开始倒计时
        while seconds_left > 0:
            logging.info(f"剩余时间: {seconds_left}秒")
            time.sleep(1)  # 暂停1秒
            seconds_left -= 1
        logging.info("倒计时结束")
        # 关闭浏览器
        driver.quit()
if __name__ == "__main__":
    main()
