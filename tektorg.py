import time
import requests
from bs4 import BeautifulSoup
from secrets import TOKEN, CHATID


URL = 'https://www.tektorg.ru/market/procedures?region=Чувашская+Республика&status=270&lang=ru&sort=datestart&limit=500'
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')

PROCEDURES = soup.find_all('div', class_='section-procurement__item')
PROCEDURE = []

if PROCEDURES:
    with open('last.txt') as f:
        last = str(f.readline()).strip()

    for item in PROCEDURES:
        title = item.find('a', class_='section-procurement__item-title')
        href = title.href

        if title.text.strip() != last:
            PROCEDURE.append(title)
            print(title, href)
        else:
            break

    to_telegram = '\n'.join(PROCEDURE)

    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=html&text=%s' % (TOKEN, CHATID, to_telegram))

    # with open('last.txt', 'w') as f:
    #     f.write(str(PROCEDURES[0].text.strip()))
    # print(str(PROCEDURES[0].text.strip()))