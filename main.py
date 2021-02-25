from datetime import datetime, date
import time
import requests
from bs4 import BeautifulSoup
import os
import os.path

current_date = date.today()
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63',
           'accept': '*/*'}


def get_html(url_get, params=None):
    r = requests.get(url_get, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    name_shares = soup.find('h1', class_='float_lang_base_1 relativeAttr').get_text()
    name_shares = name_shares.strip()

    prise = soup.find('span', class_='arial_26').get_text()
    prise = prise.replace(',', '.')

    current_quotes = soup.find('span', class_='arial_20').get_text()
    current_quotes = current_quotes.replace(',', '.')

    current_quotes2 = soup.find('div', class_='top bold inlineblock').get_text()
    current_quotes2 = current_quotes2[current_quotes2.index('%') - 5:current_quotes2.index('%') + 1]
    current_quotes2 = current_quotes2.replace(',', '.')

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


'''
def parser(url):
    html = get_html(url)

    if html.status_code == 200:
        mas = get_content(html.text)
        return mas
    else:
        print('Error')
'''


def parser(url_link):
    html = get_html(url_link)

    if html.status_code == 200:
        mas_p = get_content(html.text)
        valut = {
            'name': mas_p[0],
            'prise': mas_p[1],
            'cur_quotes': mas_p[2],
            'cur_quotes%': mas_p[3]
        }
        return valut
    else:
        print('Error')


Name = '0'
Number_Assets = '0'
Number_price = '0'
palka = chr(92)
print(palka)
# dir_f = os.path.abspath(os.curdir + palka)
#dir_f = os.path.abspath(os.curdir)
dir_f = 'D:' + palka + 'Shares'
dir_f += palka

print(dir_f)

# current_quotes = soup.find('span', class_='arial_20').get_text()
# current_quotes = soup.find('div', class_='top bold inlineblock')

currency = {
    'USD/RUB': 'https://ru.investing.com/currencies/usd-rub',
    'EUR/RUB': 'https://ru.investing.com/currencies/eur-rub',
    'USD/EUR': 'https://ru.investing.com/currencies/usd-eur',
    'EUR/USD': 'https://ru.investing.com/currencies/eur-usd'
}

url = 'https://ru.investing.com/etfs/tspx'
# for i in range(10):
#    print(parser(currency['USD/RUB']))
#    time.sleep(5)

Number = str(input('-----\nЧто вы хотите?\n'
                   '        1. Перевод валют\n'
                   '        2. Расчёт доходности  Прочитайте -> (README and Shares)\n'
                   'Введите номер (без точки). --> '))
if Number == '1':
    print('Поддерживаются: USD, EUR, RUB.')
    value_of = input('Введите из какой валюты хотите переводить: ')
    value_in = input('Введите в какую валюту хотите перевести: ')
    value = float(input('Введите число ' + str(value_of) + ': '))
    if value_in == value_of:
        print(value)
    elif value_of == 'USD' and value_in == 'EUR':
        mas = parser(currency['USD/EUR'])
        print(value * float(mas['name']))
    elif value_of == 'EUR' and value_in == 'USD':
        mas = parser(currency['EUR/USD'])
        print(value * float(mas['name']))
    elif value_of == 'RUB':
        if value_in == 'USD':
            mas = parser(currency['USD/RUB'])
            print(value / float(mas['name']))
        elif value_in == 'EUR':
            mas = parser(currency['EUR/RUB'])
            print(value / float(mas['name']))
    elif value_in == 'RUB':
        if value_of == 'USD':
            mas = parser(currency['USD/RUB'])
            print(value * float(mas['name']))
        elif value_of == 'EUR':
            mas = parser(currency['EUR/RUB'])
            print(value * float(mas['name']))

elif Number == '2':
    Number = str(input('-----\nЧто вы хотите?\n'
                       '        1. Добавить новый актив\n'
                       '        2. Сделать расчёт доходности\n'
                       '        3. Изменить текущую цену Акции\n'
                       'Введите номер (без точки). --> '))
    if Number == '1':
        link = str(input('Введите ссылку нового актива: '))
        Number_Assets = str(input('Введите количество купленных акций: '))
        Number_price = str(input('Введите стоимость за акцию: '))
        pars = parser(link)
        with open('Assets.txt', 'a') as Assets:
            Assets.write('\n' + pars['name'] + '|' + Number_Assets + '|' + Number_price + '|' + link)

    elif Number == '2':
        time.sleep(3)
        # Name = str(input('Введите название актива: '))
        print('-----')
        time.sleep(3)
        with open(str(dir_f) + 'Assets.txt', 'r') as Assets:  # Два файла отвечают за перезапись данных профилей
            print('yes')
            time.sleep(3)
            Number_ch = 0
            for line in Assets:
                Number_ch += 1
                vr = line.split('|')
                print(str(Number_ch) + '.', vr[0], '-->', vr[1], 'акция(и)')
            Number = str(input('-----\nВведите номер (без точки). --> '))
            Number_ch = 0
            for line in Assets:
                Number_ch += 1
                if Number_ch == Number:
                    vr = line.split('|')
                    break
        print('yes2')
        time.sleep(5)
        pars = parser(vr[3])
        prise_shares = float(vr[1]) * float(vr[2])
        current_price = float(vr[1]) * float(pars['prise'])
        print('-----\n'
              'Средняя цена закупки:', prise_shares, '\n'
              'Текущая цена ваших акций:', current_price, '\n'
              'Прибыль/убыток:', current_price - prise_shares)

    elif Number == '3':
        Name = str(input('Введите название актива: '))
        Number_price = str(input('Введите текущую стоимость за акцию: '))
        with open('Assets.txt', 'r') as Assets, open('system.txt', 'w') as vrem:  # Два файла отвечают за перезапись данных профилей
            for line in Assets:
                print(line)
                if line.count(Name) > 0:
                    vr = line.split(':')
                    vr[3] = Number_price
                    vrem.write(vr[0] + '|' + vr[1] + '|' + vr[2] + '|' + vr[3])
                else:
                    vrem.write(line)
        with open('Assets.txt', 'w') as Assets, open('system.txt', 'r') as vrem:
            Assets.write(vrem.read())
else:
    print('-----\nНеверное число')


'''
def Save():  # Функция для сохранения игры (баланса и профиля)
    with open('Assets.txt', 'r') as Assets, open('system.txt', 'w') as vrem:  # Два файла отвечают за перезапись данных профилей
        for line_f in Assets:
            if line_f.count(Name) > 0:
                global SaveBalance
                line_f = line.replace(str(SaveBalance), str(balance))
                SaveBalance = balance
                vrem.write(line_f)
            else:
                vrem.write(line_f)
    with open('Assets.txt', 'w') as Assets, open('system.txt', 'r') as vrem:
        Assets.write(vrem.read())
'''

'''
#from pycbrf.toolbox import ExchangeRates


# Запрашиваем данные на 26-е июня.
rates = ExchangeRates('2016-06-26')


rates.date_requested  # 2016-06-26 00:00:00
rates.date_received  # 2016-06-25 00:00:00
# 26-е был выходной, а курс на выходные установлен 25-го
rates.dates_match  # False

# Список всех курсов валют на день доступ в rates.rates.

# Поддерживаются разные идентификаторы валют:
print(rates['USD'].rate)  # Доллар США
print(rates['USD'])
rates['R01235'].name  # Доллар США
rates['840'].name  # Доллар США

# Вот, что внутри объекта ExchangeRate:
rates['USD']

    ExchangeRate(
        id='R01235',
        name='Доллар США',
        code='USD',
        num='840',
        value=Decimal('65.5287'),
        par=Decimal('1'),
        rate=Decimal('65.5287'))

'''

# URL = 'https://ru.investing.com/etfs/tspx'


# print(parser('https://ru.investing.com/currencies/usd-rub'))


time.sleep(10)
