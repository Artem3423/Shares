from datetime import datetime, date
from myparser import parser
# import time
import config

Name = '0'
Number_Assets = '0'
Number_price = '0'

palka = chr(92)
print(palka)
dir_f = config.WAY
# dir_f = os.path.abspath(os.curdir + palka)
# dir_f = os.path.abspath(os.curdir)
# dir_f = 'D:' + palka + 'Shares'
# dir_f += palka

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
current_date = date.today()
Number = ''
if Number == '':
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
            print(value * float(mas[1]))
        elif value_of == 'EUR' and value_in == 'USD':
            mas = parser(currency['EUR/USD'])
            print(value * float(mas[1]))
        elif value_of == 'RUB':
            if value_in == 'USD':
                mas = parser(currency['USD/RUB'])
                print(value / float(mas[1]))
            elif value_in == 'EUR':
                mas = parser(currency['EUR/RUB'])
                print(value / float(mas[1]))
        elif value_in == 'RUB':
            if value_of == 'USD':
                mas = parser(currency['USD/RUB'])
                print(value * float(mas[1]))
            elif value_of == 'EUR':
                mas = parser(currency['EUR/RUB'])
                print(value * float(mas[1]))

    elif Number == '2':
        Number = str(input('-----\nЧто вы хотите?\n'
                           '        1. Добавить новый актив\n'
                           '        2. Сделать расчёт доходности\n'
                           '        3. Добавить/удалить часть акций\n'
                           'Введите номер (без точки). --> '))
        if Number == '1':
            link = str(input('Введите ссылку нового актива: '))
            Number_Assets = str(input('Введите количество купленных акций: '))
            Number_price = str(input('Введите стоимость за акцию: '))
            pars = parser(link)
            with open(str(dir_f) + 'Assets.txt', 'a') as Assets:
                Assets.write('\n' + pars['name'] + '|' + Number_Assets + '|' + Number_price + '|' + link)

        elif Number == '2':
            print('-----')
            with open(str(dir_f) + 'Assets.txt', 'r') as Assets:  # Два файла отвечают за перезапись данных профилей
                Number_ch = 0
                for line in Assets:
                    Number_ch += 1
                    A_list = line.split('|')
                    print(str(Number_ch) + '.', A_list[0], '-->', A_list[1], 'акция(и)')
                Number = str(input('-----\nВведите номер (без точки). --> '))
                Number_ch = 0
                for line in Assets:
                    Number_ch += 1
                    if Number_ch == Number:
                        A_list = line.split('|')
                        break
            pars = parser(A_list[3])
            prise_shares = float(A_list[1]) * float(A_list[2])
            current_price = float(A_list[1]) * float(pars['prise'])
            print('-----\n'
                  'Средняя цена закупки:', prise_shares, '\n'
                  'Текущая цена ваших акций:', current_price, '\n'
                  'Прибыль/убыток:', current_price - prise_shares)

        elif Number == '3':
            print('-----')
            with open(str(dir_f) + 'Assets.txt', 'r') as Assets:  # Два файла отвечают за перезапись данных профилей
                Number_ch = 0
                for line in Assets:
                    Number_ch += 1
                    A_list = line.split('|')
                    print(str(Number_ch) + '.', A_list[0], '-->', A_list[1], 'акция(и)')
                Number = int(input('-----\nВведите номер (без точки). --> '))
                Number_ch = 0
            with open(str(dir_f) + 'Assets.txt', 'r') as Assets:
                for line in Assets:
                    Number_ch += 1
                    if Number_ch == Number:
                        A_list = line.split('|')
                        break
            print('Количество проданных акций писать с минусом. Пример: -632')
            Number_Assets = str(input('Введите количество купленных/проданных акций: '))
            Number_price = str(input('Введите стоимость за акцию: '))
            old_prise = A_list[2]
            if Number_Assets.count('-') == 1:
                old_assets = A_list[1]
                old_AllPrise = float(A_list[1]) * float(A_list[2])
                A_list[1] = str(int(A_list[1]) + int(Number_Assets))
                print('-----\n', A_list[0], 'Кол-во акций:', old_assets, '-->', A_list[1], '\n'
                      'Общая цена акций:', old_AllPrise, '-->', float(A_list[1]) * float(A_list[2]))
            else:
                old_assets = A_list[1]
                old_AllPrise = float(A_list[1]) * float(A_list[2])
                A_list[1] = str(int(A_list[1]) + int(Number_Assets))

                new_AllPrise = float(Number_Assets) * float(Number_price)
                AllPrise = old_AllPrise + new_AllPrise

                Number_price = AllPrise / float(A_list[1])
                A_list[2] = str(Number_price)

                print('-----\n', A_list[0], 'Кол-во акций:', old_assets, '-->', A_list[1], '\n'
                      'Общая цена акций:', old_AllPrise, '-->', AllPrise)
            with open(str(dir_f) + 'Assets.txt', 'r') as Assets, open(str(dir_f) + 'system.txt', 'w') as system:  # Два файла отвечают за перезапись данных профилей
                for line in Assets:
                    if line.count(A_list[0] + '|' + old_assets + '|' + old_prise) == 1:
                        line = A_list[0] + '|' + A_list[1] + '|' + A_list[2] + '|' + A_list[3]
                        system.write(line)
                    else:
                        system.write(line)
            with open(str(dir_f) + 'Assets.txt', 'w') as Assets, open(str(dir_f) + 'system.txt', 'r') as system:
                Assets.write(system.read())
    else:
        print('-----\nНеверное число')

    Number = input('-----\nНажмите ENTER что бы начать заново. Или ПРОБЕЛ и ENTER что бы закрыть это окно.')
