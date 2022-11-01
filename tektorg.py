import time
import requests
from bs4 import BeautifulSoup
from secrets import TOKEN, CHATID


URL = 'https://www.tektorg.ru/market/procedures?region=Чувашская+Республика&status=270&lang=ru&sort=datestart&limit=500'
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')

LINKS = soup.find_all('a', class_='section-procurement__item-title')

if LINKS:
    with open('last.txt') as f:
        last_title = str(f.readline()).strip()

    for link in LINKS:
        if link.text.strip() != last_title:
            # print(link.text)
            requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=html&text=%s' % (TOKEN, CHATID, link.text))
            if len(LINKS) > 1:
                time.sleep(1)
        else:
            break

    with open('last.txt', 'w') as f:
        f.write(str(LINKS[0].text.strip()))
