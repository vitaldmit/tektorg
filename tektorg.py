import time
import requests
from bs4 import BeautifulSoup
from secrets import TOKEN, CHATID


URL = 'https://www.tektorg.ru/market/procedures?status=270&region=%D0%A7%D1%83%D0%B2%D0%B0%D1%88%D1%81%D0%BA%D0%B0%D1%8F+%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0&lang=ru&sort=datestart&order=desc&limit=500'
# URL = 'https://www.tektorg.ru/market/procedures?q=%D0%AF%D0%BD%D1%82%D0%B8%D0%BA%D0%BE%D0%B2&region=%D0%A7%D1%83%D0%B2%D0%B0%D1%88%D1%81%D0%BA%D0%B0%D1%8F+%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0&status=270&lang=ru&sort=datestart&limit=500'
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
items = []

LINKS = soup.find_all('a', class_='section-procurement__item-title')

if LINKS:
    with open('last.txt', 'r') as f:
        last = str(f.readline()).strip()

    i = 1
    for link in LINKS:
        if link.text.strip() != last:
            items.append(f"{i}) {link.text}: https://www.tektorg.ru{link['href']}")
            i+=1
        else:
            break

    to_telegram = '\n\n'.join(str(v) for v in items)
    # requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=html&text=%s' % (TOKEN, CHATID, to_telegram))
    print(to_telegram)

    with open('last.txt', 'w') as f:
        f.write(str(LINKS[0].text.strip()))

