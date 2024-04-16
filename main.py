from selenium import webdriver
import time
from fake_useragent import UserAgent

#settings
useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.random}")

#stast
driver = webdriver.Chrome(
    options=options
)
driver.get('https://www.whatismybrowser.com/')
time.sleep(100)




# # Аутентификационные данные
# proxy = {
#     'http': 'http://wCxdCQ:gXaCbs@147.45.62.30:8000',
# }

