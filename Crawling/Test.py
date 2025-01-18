from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)

# driver.get('https://example.com')
# driver.get('https://zoodkomak.com/blog/pages/FreeContent/Adsl-disconnection-problem')
driver.get('https://facebook.com')

user_name = element = driver.find_element(By.ID, 'email')
user_name.send_keys('ehsanmotamedi12345@yahoo.com')

password = element = driver.find_element(By.ID, 'pass')
password.send_keys('1234576')

btnlogin = driver.find_element(By.NAME, 'login')
btnlogin.click()

# print(element.text)  # Extract text content

elements = driver.find_elements(By.CLASS_NAME, 'class_name')
for element in elements:
    print(element.text)

button = driver.find_element(By.NAME, 'button_name')
button.click()


