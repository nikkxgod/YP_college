import requests
from bs4 import BeautifulSoup as BS

r = requests.get("https://www.cloudbet32.com/ru/esports/counter-strike/international-t987e-cct-europe-qualifier/23189956/c1c46f5-ruby-v-ce75da-zero-tenacity")
html = BS(r.content, 'html.parser')

result = html.find_all('data-component'=="market-tab")
for i in result:
    print(i.text)
