from fake_useragent import UserAgent
import requests as r
import json


# print(ua.random)


def money(surname):
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

            url = f'https://cs.money/1.0/market/sell-orders?limit=60&name={surname}&offset={item}&order=asc&sort=price'

            response = r.get(
                url=url,
                headers={'user-agent': f'{ua.random}'}
            )

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
                        {"Имя": name, "Цена": price, "Ссылка": link, "Качество": qualit})

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


def buff(type):
    global result_buff
    result_buff = []
    ses = r.session()
    headers = {
        'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    cookies = {'Cookie': 'Device-Id=YWMPHEIk3KsETz2FrFr2; Locale-Supported=ru; game=csgo; NTES_YD_SESS=QjPvrQC69SZp.iaASkTmBwQ3u9bSiBA56gQ1zBKXJJpC1NC0kvPBVz89uK4hrLeAVMitNCpZ2i9N9R5wlNEmazv_W8F7L7BVGY1cUGk3AJohWG05SBfR4YWQx.ic3h3vJsSu5kHkVBKC7D_04o3HUeTexEGJBzNwrl1UL87mzi1onFCF7kU6y6nzPxD0AR96mqrH6QQUWk0rocOxQsSfPB4dsnB4j99In0aTIeDfhh_Fh; S_INFO=1672432915|0|0&60##|7-9061071451; P_INFO=7-9061071451|1672432915|1|netease_buff|00&99|null&null&null#not_found&null#10#0|&0|null|7-9061071451; session=1-CvAy8kKQWtuRLMnVZUeM5z9o4eRd61nojKSZ-yccof7c2032323821; csrf_token=ImUwNDg3OGE0MWM5ODIxYWVjMDBmZmIzZTU5NDcxZDAzYzQxOWJjMmEi.FpDeyQ.22M03GWVe-k_3Mc0r3qfv90FxcQ', 'Set-Cookie': 'session = 1-CvAy8kKQWtuRLMnVZUeM5z9o4eRd61nojKSZ-yccof7c2032323821 HttpOnly; Path = /',
               'Set-Cookie': 'csrf_token=ImUwNDg3OGE0MWM5ODIxYWVjMDBmZmIzZTU5NDcxZDAzYzQxOWJjMmEi.FpDgKA.3fTcqJsxokKMxk89R25OLWT-vbU; Path=/'



               }

    response = ses.get(
        url=f'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search={type}&use_suggestion=0&_=1672413193794', cookies=cookies, headers=headers)

    data = response.json()
    page = data['data']['total_page']
    page = int(page)

    count = 0
    for item in range(1, page+1):
        count += 1
        response = ses.get(
            url=f'https://buff.163.com/api/market/goods?game=csgo&page_num={item}&search={type}&use_suggestion=0&_=1672413193794', headers=headers, cookies=cookies)

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
                    result_buff.append(
                        {"Имя": name, "Цена": price, "Качество": quality_ready})

                except:
                    pass
    return (result_buff)


def together():
    money(surname="knife")
    buff(type="knife")
    print(len(result_money))
    print(len(result_buff))
    for results_money in result_money:
        name = results_money['Имя']
        link = results_money['Ссылка']
        price = results_money['Цена']
        quality = results_money["Качество"]
        for results_buff in result_buff:
            if name in results_buff["Имя"] and quality in results_buff['Качество']:
                print(link)


def main():
    together()


if __name__ == '__main__':
    main()
