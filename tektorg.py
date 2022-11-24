import requests
from bs4 import BeautifulSoup

from secrets import TOKEN, CHATID


URL = 'https://www.tektorg.ru/market/procedures?status=270&region=%D0%A7%D1%83%D0%B2%D0%B0%D1%88%D1%81%D0%BA%D0%B0%D1%8F+%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0&lang=ru&sort=datestart&order=desc&limit=500'

page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
messages = []

ITEMS = soup.find_all('div', {'class': 'section-procurement__item-info'})
LAST_ITEM = ITEMS[0].find('a', {'class': 'section-procurement__item-title'})

if ITEMS:
    with open('last.txt', 'r', encoding='utf-8') as f:
        last = str(f.readline()).strip()

    for item in ITEMS:
        link = item.find('a', {'class': 'section-procurement__item-title'})
        price = item.find('div', {'class': 'section-procurement__item-totalPrice'})
        if link.text.strip() != last:
            messages.append(f"[{link.text}](https://www.tektorg.ru{link['href']}) *{price.text}*")
        else:
            break

    to_telegram = '\n\n'.join(str(m) for m in messages)
    response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=Markdown&text=%s' % (TOKEN, CHATID, to_telegram))

    with open('last.txt', 'w', encoding='utf-8') as f:
        f.write(str(LAST_ITEM.text.strip()))

