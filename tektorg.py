import json
import requests

from secrets import TOKEN, CHATID

def getProcedures(city):
    URL = 'https://www.tektorg.ru/api/getProcedures'
    req_dict = {"params":{"sectionsCodes[0]":"market","name":city,"status[0]":"Приём заявок","page":1,"sort":"datePublished_desc"}}
    headers = { 'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://www.tektorg.ru',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                }


    res = requests.post(URL, headers=headers, json=req_dict)

    # Convert to dict
    json_acceptable_string = res.text.replace("'", "\"")
    dataList = json.loads(json_acceptable_string)

    list_of_procedures = dataList['data']
    first_id = str(list_of_procedures[0]['id'])
    messages = []

    if res and list_of_procedures:
        with open(city + '.txt', 'r', encoding='utf-8') as f:
            last_id = str(f.readline()).strip()

        for procedure in list_of_procedures:
            if str(procedure['id']) != last_id:
                messages.append(f"[{procedure['title']}](https://www.tektorg.ru/market/procedures/{procedure['id']}) *{procedure['sumPrice']}* `{procedure['organizerName']}`")
            else:
                break

        to_telegram = '\n\n'.join(str(m) for m in messages)

        if len(to_telegram) > 4096:
            for x in range(0, len(to_telegram), 4096):
                requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=Markdown&text=%s' % (TOKEN, CHATID, to_telegram[x:x+4096]))
                # print(to_telegram[x:x+4096])
        else:
            requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=Markdown&text=%s' % (TOKEN, CHATID, to_telegram))
            # print(to_telegram)

        with open(city + '.txt', 'w', encoding='utf-8') as f:
            f.write(first_id.strip())


if __name__ == '__main__':
    getProcedures('Янтиков')
    getProcedures('Канаш')
