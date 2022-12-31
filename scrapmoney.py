from fake_useragent import UserAgent
import requests as r
import json


# print(ua.random)


def money(surname, maxim, minim):

    ua = UserAgent()
    global result_money
    result_money = []
    offset = 0
    batch_size = 60
    result = []
    count = 0
    stoping = True
    while stoping:
        for item in range(offset, offset + batch_size, 60):

            url = f'https://cs.money/1.0/market/sell-orders?limit=60&maxPrice={maxim/ 7.11}&minPrice={minim / 7.11}&name={surname}&offset={item}'
            # awpprint(url)
            response = r.get(
                url=url,
                headers={'user-agent': f'{ua.random}'}
            )
            # print(response.status_code)
            offset += batch_size
            if response.status_code == 200:

                data = response.json()

                try:
                    x = data['errors']
                    stoping = False
                    break

                except:
                    pass
                for i in data['items']:
                    name = i['asset']['names']['full'].split("(")[0]
                    price = i['pricing']['computed']
                    link = i['links']['3d']
                    qualit = i['asset']['quality']
                    result_money.append(
                        {"Имя": name, "Цена": float(price)*7.11, "Ссылка": link, "Качество": qualit})
                    #print(name, price, link)
            else:
                try:
                    data = response.json()
                    try:
                        x = data['errors']
                        stoping = False
                        break

                    except:
                        pass
                except:
                    stoping = False
                    break

    return (result_money)


def buff(surname):
    global result_buff
    result_buff = []
    ses = r.session()
    headers = {
        'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    cookies = {'Cookie': 'Device-Id=z9OIAlHs3Pr9m4roz1np; Locale-Supported=ru; game=csgo; NTES_YD_SESS=jnR9zvTqv9ifCza4Rq9FPZchEBjEOWamOajTk2LMBBRAT7Ap0cd2FkeKm35j9PJVCOzt3aqCo_vswAadrtJwT_nQs4O462vaIkQYTCPoVAKj1_OxdQIr1goj1suDXQXcBnrmP0x0F2LAEI3peqXxvJ9J1_4B2k7SUwTvogE8kuTqkHjBER117.XrnxdHZ_gTa1.CcDaH4zzLvpanUw5t_GxU8OQrXhfm2bMBMv931rn2Q; S_INFO=1672446971|0|0&60##|7-9649586377; P_INFO=7-9649586377|1672446971|1|netease_buff|00&99|null&null&null#not_found&null#10#0|&0||7-9649586377; session=1-tgMiscVPAaIUux1yefQdOkaPUL6y5Q67RjXqg5BbPLRR2032335371; csrf_token=ImY2Y2Y4MGRlYTdhZDdiNWNjZjlmOTczZWZjZjc0MTJhYmQxMzM2ZmEi.FpEXjQ.3X_GGW-DkG2Yek0rXlcTvspAeFE', 'Set-Cookie': 'session=1-tgMiscVPAaIUux1yefQdOkaPUL6y5Q67RjXqg5BbPLRR2032335371; HttpOnly; Path=/',
               'Set-Cookie': 'csrf_token=ImY2Y2Y4MGRlYTdhZDdiNWNjZjlmOTczZWZjZjc0MTJhYmQxMzM2ZmEi.FpEXnQ.Ea4Mljn2jR42J1xUWBtCW8rEgPQ; Path=/'



               }

    response = ses.get(
        url=f'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search={surname}&use_suggestion=0&_=1672413193794', cookies=cookies, headers=headers)
    print(response.text)
    data = response.json()
    page = data['data']['total_page']
    page = int(page)

    count = 0
    for item in range(1, page+1):
        count += 1
        response = ses.get(
            url=f'https://buff.163.com/api/market/goods?game=csgo&page_num={item}&search={surname}&use_suggestion=0&_=1672413193794', headers=headers, cookies=cookies)

        if response.status_code == 200:
            data = response.json()
            for i in data['data']['items']:
                try:
                    name = i['short_name'].split("(")[0]

                    price = i['sell_min_price']
                    # link = i['links']['3d']

                    qualit = i['goods_info']['info']['tags']['exterior']['localized_name']

                    if "-" in qualit:
                        qualit = qualit.replace("-", " ")
                    quality2 = []
                    for quality in qualit.split():
                        quality2.append(quality[0].lower())
                    quality_ready = "".join(quality2)
                    quality2.clear()
                    # print(price)
                    result_buff.append(
                        {"Имя": name, "Цена": price, "Качество": quality_ready})

                except:
                    pass
    return (result_buff)


def together():

    fetch = "gloves \nknife\nawp\nm4a1\nm4a1-s\nak-47\nglock\nusp-s\ndesert eagle\naug\nssg 08\nfamas\ngalil ar"
    print(fetch)
    j = str(input("Введите тип оружия для парсинга:  "))
    min_price = int(input("Введите минимальную цену:  "))
    max_price = int(input("Введите максимальную цену:  "))
    percent = int(input("Введите процент:  "))

    money(surname=j, maxim=max_price, minim=min_price)
    buff(surname=j)
    # print(len(result_money))
    # print(len(result_buff))

    for results_money in result_money:
        name = results_money['Имя']
        link = results_money['Ссылка']
        price = results_money['Цена']
        quality = results_money["Качество"]
        for results_buff in result_buff:
            if name == results_buff["Имя"] and quality == results_buff['Качество']:
                discount = (
                    ((float(price)*0.97)-float(results_buff['Цена']))/float(price))*100
                if discount >= percent and discount < 25:
                    print(
                        f"Кс мани. Цена: {price}. Имя: {name}. Качество: {quality} Ссылка: {link}")
                    print(
                        f"Buff. Цена: {results_buff['Цена']} .Имя: {results_buff['Имя']}. Качество {results_buff['Качество']}")
                    print(f"Процент скидки:  {discount}")
    k = str(input("Нажмите любую кнопку для выхода"))
    # print(results_buff['Цена'])
    # discount = (
    #     abs((float(price)-float(results_buff["Цена"]))/float(price))*100)
    # if discount >= percent and discount < 60:

    #     print(
    #         f"Название: {name}. Цена: {price}  Ссылка:  {link} ")
    #     print(discount)


def main():
    together()


if __name__ == '__main__':
    main()
