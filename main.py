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

# url = 'https://www.cloudbet32.com/ru/sports/tennis/today'  # URL сайта, к которому делаем запрос

# try:
#     response = requests.get(url, proxies=proxy)
#     # Обработка ответа
#     if response.status_code == 200:
#         print(response.text)
#     else:
#         print("Ошибка при запросе:", response.status_code)
# except requests.exceptions.RequestException as e:
#     print("Ошибка при выполнении запроса:", e)
