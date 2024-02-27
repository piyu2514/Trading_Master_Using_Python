from requests import Request, Session
import json
from prettytable import PrettyTable
from termcolor import colored


def MyFunc2():
    print("\n" * 10)
    file = open('Portfolio.txt', 'r')

    Symbols = []
    Quantity = []
    Buy_price = []

    for line in file.readlines()[1:]:
        line = line.split(',')
        Symbols.append(line[0])
        Quantity.append(float(line[1]))
        Buy_price.append(float(line[2]))

    '''
    print(Symbols)
    print(Quantity)
    print(Buy_price)
    '''

    api = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    p1 = {
        'id': '1'
    }

    p2 = {
        'id': '1376'
    }

    p3 = {
        'id': '463'
    }

    p4 = {
        'id': '1787'
    }

    p5 = {
        'id': '3252'
    }

    p6 = {
        'id': '5028'
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '8da10793-c1e9-4dce-8917-91b573eb0560',
    }
    session = Session()
    session.headers.update(headers)

    # response = session.get(api, params=parameters)
    # data = json.loads(response.text)['data']

    table = PrettyTable()
    table.field_names = ["Name", "Quantity", "Buy Price", "Current price", "Profit %", "Change 1h", "Change 1d",
                         "Change 7d"]

    def color(nr):
        if nr > 0:
            return ('\033[92m' + str(nr) + '\033[0m')  # Green Color
        else:
            return ('\033[91m' + str(nr) + '\033[0m')  # Red Color

    symbols_id = [1, 1376, 463, 1787, 3252, 5028]

    buy_value = 0
    current_value = 0

    response = session.get(api, params=p1)
    data = json.loads(response.text)['data']
    current_price = float(data['1']['quote']['USD']['price'])
    change_1h = float(data['1']['quote']['USD']['percent_change_1h'])
    change_1d = float(data['1']['quote']['USD']['percent_change_24h'])
    change_7d = float(data['1']['quote']['USD']['percent_change_7d'])

    profit = round(current_price / Buy_price[0] * 100 - 100, 2)

    buy_value += Buy_price[0] * Quantity[0]
    current_value += current_price * Quantity[0]

    table.add_row([Symbols[0], Quantity[0], Buy_price[0],
                   current_price, color(profit), color(change_1h),
                   color(change_1d), color(change_7d)])

    response = session.get(api, params=p2)
    data = json.loads(response.text)['data']
    current_price = float(data['1376']['quote']['USD']['price'])
    change_1h = float(data['1376']['quote']['USD']['percent_change_1h'])
    change_1d = float(data['1376']['quote']['USD']['percent_change_24h'])
    change_7d = float(data['1376']['quote']['USD']['percent_change_7d'])

    profit = round(current_price / Buy_price[1] * 100 - 100, 2)

    buy_value += Buy_price[1] * Quantity[1]
    current_value += current_price * Quantity[1]

    table.add_row([Symbols[1], Quantity[1], Buy_price[1],
                   current_price, color(profit), color(change_1h),
                   color(change_1d), color(change_7d)])

    response = session.get(api, params=p3)
    data = json.loads(response.text)['data']
    current_price = float(data['463']['quote']['USD']['price'])
    change_1h = float(data['463']['quote']['USD']['percent_change_1h'])
    change_1d = float(data['463']['quote']['USD']['percent_change_24h'])
    change_7d = float(data['463']['quote']['USD']['percent_change_7d'])

    profit = round(current_price / Buy_price[2] * 100 - 100, 2)

    buy_value += Buy_price[2] * Quantity[2]
    current_value += current_price * Quantity[2]

    table.add_row([Symbols[2], Quantity[2], Buy_price[2],
                   current_price, color(profit), color(change_1h),
                   color(change_1d), color(change_7d)])

    response = session.get(api, params=p4)
    data = json.loads(response.text)['data']
    current_price = float(data['1787']['quote']['USD']['price'])
    change_1h = float(data['1787']['quote']['USD']['percent_change_1h'])
    change_1d = float(data['1787']['quote']['USD']['percent_change_24h'])
    change_7d = float(data['1787']['quote']['USD']['percent_change_7d'])

    profit = round(current_price / Buy_price[3] * 100 - 100, 2)

    buy_value += Buy_price[3] * Quantity[3]
    current_value += current_price * Quantity[3]

    table.add_row([Symbols[3], Quantity[3], Buy_price[3],
                   current_price, color(profit), color(change_1h),
                   color(change_1d), color(change_7d)])

    response = session.get(api, params=p5)
    data = json.loads(response.text)['data']
    current_price = float(data['3252']['quote']['USD']['price'])
    change_1h = float(data['3252']['quote']['USD']['percent_change_1h'])
    change_1d = float(data['3252']['quote']['USD']['percent_change_24h'])
    change_7d = float(data['3252']['quote']['USD']['percent_change_7d'])

    profit = round(current_price / Buy_price[4] * 100 - 100, 2)

    buy_value += Buy_price[4] * Quantity[4]
    current_value += current_price * Quantity[4]

    table.add_row([Symbols[4], Quantity[4], Buy_price[4],
                   current_price, color(profit), color(change_1h),
                   color(change_1d), color(change_7d)])

    response = session.get(api, params=p6)
    data = json.loads(response.text)['data']
    current_price = float(data['5028']['quote']['USD']['price'])
    change_1h = float(data['5028']['quote']['USD']['percent_change_1h'])
    change_1d = float(data['5028']['quote']['USD']['percent_change_24h'])
    change_7d = float(data['5028']['quote']['USD']['percent_change_7d'])

    profit = round(current_price / Buy_price[5] * 100 - 100, 2)

    buy_value += Buy_price[5] * Quantity[5]
    current_value += current_price * Quantity[5]

    table.add_row([Symbols[5], Quantity[5], Buy_price[5],
                   current_price, color(profit), color(change_1h),
                   color(change_1d), color(change_7d)])

    print(table)
    print()

    total_profit = current_value / buy_value * 100 - 100
    dollars = current_value - buy_value

    current_value = round(float(current_value), 2)
    total_profit = round(float(total_profit), 2)
    dollars = round(float(dollars), 2)

    print(colored("PORTFOLIO VALUE", 'cyan', attrs=['bold', 'underline']) + " : " + colored("$ " + str(current_value),
                                                                                            'blue'))
    print()
    print(colored("TOTAL PROFIT", 'cyan', attrs=['bold', 'underline']) + " : " + colored(str(total_profit) + " %",
                                                                                         'blue'))
    print()
    print(colored("TOTAL PROFIT (USD)", 'cyan', attrs=['bold', 'underline']) + " : " + colored("$ " + str(dollars),
                                                                                               'blue'))

