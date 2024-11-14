import requestium

from requestium import Session, Keys

# 创建一个Requestium会话
s = Session()

# 访问登录页面
s.driver.get('https://example.com/login')

# 输入用户名和密码
s.driver.find_element_by_name('username').send_keys('testuser')
s.driver.find_element_by_name('password').send_keys('password123')

# 点击登录按钮
s.driver.find_element_by_css_selector('button[type="submit"]').click()

# 验证登录成功
welcome_message = s.driver.find_element_by_css_selector('.welcome-message').text
assert '欢迎回来，testuser' in welcome_message

# 关闭会话
s.driver.quit()