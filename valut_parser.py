import requests
from bs4 import BeautifulSoup


URL = 'https://ru.investing.com/currencies/single-currency-crosses'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63',
           'accept': '*/*'}


def get_html(url_get, params=None):
    r = requests.get(url_get, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    for i in range(1, 1000000):
        if str(soup.find('tr', id='pair_'+str(i))).count(str(i)) == 0:
            continue
        print(i)
        pair = soup.find('tr', id='pair_'+str(i))
        #print(pair)
        #if pair is None:
        #    continue
        name = pair.find('td', class_='bold left noWrap elp plusIconTd').get_text()
        #name2 = name.find('a', herf_='/currencies/eur-usd')
        #print(name)

    prise = soup.find('span', class_='arial_26').get_text()

    current_quotes = soup.find('span', class_='arial_20').get_text()

    current_quotes2 = soup.find('div', class_='top bold inlineblock').get_text()
    current_quotes2 = current_quotes2[current_quotes2.index('%') - 5:current_quotes2.index('%') + 1]

    '''
    items = soup.find_all('a', class_='na-card-item')

    cars = []
    for item in items:
        uah_price = item.find('span', class_='size15')
        if uah_price:
            uah_price = uah_price.get_text().replace(' • ', '')
        else:
            uah_price = 'Цену уточняйте'
        cars.append({
            'title': item.find('div', class_='na-card-name').get_text(strip=True),
            'link': HOST + item.find('span', class_='link').get('href'),
            'usd_price': item.find('strong', class_='green').get_text(),
            'uah_price': uah_price,
            'city': item.find('svg', class_='svg_i16_pin').find_next('span').get_text(),
        })
    return cars
 '''
    return name_shares, prise, current_quotes, current_quotes2


def parser(url):
    html = get_html(url)

    if html.status_code == 200:
        mas = get_content(html.text)
        return mas
    else:
        print('Error')


parser(URL)
#parse('https://ru.investing.com/etfs/tspx')