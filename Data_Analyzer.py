import threading
import time
from termcolor import colored
from prettytable import PrettyTable
import requests


def MyFunc4():
    print("\n" * 10)
    api = "https://api.binance.com/api/v3/ticker/24hr"

    api_klines_1m = "https://api.binance.com/api/v3/klines?interval=1m&limit=1000&symbol="  # 1000 minutes data
    api_klines_1d = "https://api.binance.com/api/v3/klines?interval=1d&limit=1000&symbol="  # 1000 days data

    symbols = []
    indexes = []

    data = requests.get(api).json()

    minimum_volume = 100

    for currency in data:
        if "BTC" in currency['symbol'] and float(currency['quoteVolume']) > minimum_volume:
            symbols.append(currency['symbol'])
            indexes.append(data.index(currency))

    prices_1m = [[] for each in range(len(symbols))]
    prices_1d = [[] for each in range(len(symbols))]

    print()
    print("Found " + colored(len(symbols), 'green') + " Cryptocurrencies that were traded the most in the last 24 "
                                                      "hours.")
    time.sleep(2)
    print("Getting Data .....")
    time.sleep(3)
    print("Running Analyzer .......")
    print()

    def kline_calculate(api):
        prices = [[] for each in range(len(symbols))]

        for symbol in symbols:
            temp_api = api_klines_1m + symbol
            candlesticks = requests.get(temp_api).json()
            for candle in candlesticks:
                prices[symbols.index(symbol)].append(float(candle[1]))
        #   print(prices[symbols.index(symbol)])
        return prices

    prices_1m = kline_calculate(api_klines_1m)
    prices_1d = kline_calculate(api_klines_1d)

    current_price = [0 for x in range(len(symbols))]
    current_score = [0 for x in range(len(symbols))]

    change_2m = [0 for x in range(len(symbols))]
    change_6h = [0 for x in range(len(symbols))]
    change_12h = [0 for x in range(len(symbols))]

    change_30d = [0 for x in range(len(symbols))]
    change_1y = [0 for x in range(len(symbols))]

    moving_average_30m = [0 for x in range(len(symbols))]
    moving_average_30d = [0 for x in range(len(symbols))]

    def kline_continuum():
        seconds = 0

        while True:
            data = requests.get(api).json()

            i = 0

            for index in indexes:
                current_price[i] = float(data[index]['lastPrice'])
                if seconds % 60 == 0:
                    prices_1m[i].append(current_price[i])
                i += 1
            time.sleep(5)
            seconds += 5

    def calculate_change(current_price, list, index):
        try:
            result = round(current_price * 100 / list[index] - 100, 2)
        except:
            return 0

        return result

    def color(nr):
        if nr > 0:
            return ('\033[92m' + str(nr) + '\033[0m')  # Green Color
        else:
            return ('\033[91m' + str(nr) + '\033[0m')  # Red Color

    def calculate_score():
        for symbol in range(len(symbols)):
            change_2m[symbol] = calculate_change(current_price[symbol], prices_1m[symbol], -2)
            change_6h[symbol] = calculate_change(current_price[symbol], prices_1m[symbol], -360)
            change_12h[symbol] = calculate_change(current_price[symbol], prices_1m[symbol], -720)
            change_30d[symbol] = calculate_change(current_price[symbol], prices_1d[symbol], -30)
            change_1y[symbol] = calculate_change(current_price[symbol], prices_1d[symbol], -365)

            average_30m = sum(prices_1m[symbol][-30:]) / 30
            average_30d = sum(prices_1d[symbol][-30:]) / 30

            moving_average_30m[symbol] = round(current_price[symbol] * 100 / average_30m - 100, 2)
            moving_average_30d[symbol] = round(current_price[symbol] * 100 / average_30d - 100, 2)

        for symbol in range(len(symbols)):
            score = 0
            a = change_2m[symbol]
            if 0 < a < 0.5:
                score += 1
            elif 0.5 <= a:
                score += 1.25

            a = change_6h[symbol]
            if 0 < a < 0.5:
                score += 1
            elif 0.5 <= a:
                score += 1.25

            a = change_12h[symbol]
            if 0 < a < 0.5:
                score += 1
            elif 0.5 <= a:
                score += 1.25

            a = change_30d[symbol]
            if 0 < a < 10:
                score += 1.25
            elif 10 <= a:
                score += 1.75

            a = change_1y[symbol]
            if 0 < a < 20:
                score += 1.25
            elif 20 <= a:
                score += 1.75

            a = moving_average_30m[symbol]
            if 0 < a < 0.5:
                score += 1
            elif 0.5 <= a < 1:
                score += 1.25

            a = moving_average_30d[symbol]
            if 0 < a < 0.5:
                score += 1
            elif 0.5 <= a < 1:
                score += 1.25

            current_score[symbol] = score

    def print_results():
        sort_index = 0
        count = 0
        while count < 5:
            calculate_score()

            toggle_sort = [current_score, change_2m, change_6h, change_12h, change_30d, change_1y,
                           moving_average_30m, moving_average_30d]

            sort_by = toggle_sort[sort_index % len(toggle_sort)]

            sorted_data = sorted(range(len(sort_by)), key=lambda k: sort_by[k])
            sorted_data.reverse()

            table = PrettyTable()
            if (sort_index % len(toggle_sort) == 0):
                table.field_names = [colored('Symbol', 'blue'), colored('Score', 'magenta'), colored('2m_ch', 'blue'),
                                     colored('6h_ch', 'blue'), colored('12h_ch', 'blue'), colored('30d_ch', 'blue'),
                                     colored('1y_ch', 'blue'), colored('30m_MA', 'blue'), colored('30d_MA', 'blue'),
                                     colored('Price', 'blue')]
            elif (sort_index % len(toggle_sort) == 1):
                table.field_names = [colored('Symbol', 'blue'), colored('Score', 'blue'), colored('2m_ch', 'magenta'),
                                     colored('6h_ch', 'blue'), colored('12h_ch', 'blue'), colored('30d_ch', 'blue'),
                                     colored('1y_ch', 'blue'), colored('30m_MA', 'blue'), colored('30d_MA', 'blue'),
                                     colored('Price', 'blue')]
            elif (sort_index % len(toggle_sort) == 2):
                table.field_names = [colored('Symbol', 'blue'), colored('Score', 'blue'), colored('2m_ch', 'blue'),
                                     colored('6h_ch', 'magenta'), colored('12h_ch', 'blue'), colored('30d_ch', 'blue'),
                                     colored('1y_ch', 'blue'), colored('30m_MA', 'blue'), colored('30d_MA', 'blue'),
                                     colored('Price', 'blue')]
            elif (sort_index % len(toggle_sort) == 3):
                table.field_names = [colored('Symbol', 'blue'), colored('Score', 'blue'), colored('2m_ch', 'blue'),
                                     colored('6h_ch', 'blue'), colored('12h_ch', 'magenta'), colored('30d_ch', 'blue'),
                                     colored('1y_ch', 'blue'), colored('30m_MA', 'blue'), colored('30d_MA', 'blue'),
                                     colored('Price', 'blue')]
            elif (sort_index % len(toggle_sort) == 4):
                table.field_names = [colored('Symbol', 'blue'), colored('Score', 'blue'), colored('2m_ch', 'blue'),
                                     colored('6h_ch', 'blue'), colored('12h_ch', 'blue'), colored('30d_ch', 'magenta'),
                                     colored('1y_ch', 'blue'), colored('30m_MA', 'blue'), colored('30d_MA', 'blue'),
                                     colored('Price', 'blue')]
            elif (sort_index % len(toggle_sort) == 5):
                table.field_names = [colored('Symbol', 'blue'), colored('Score', 'blue'), colored('2m_ch', 'blue'),
                                     colored('6h_ch', 'blue'), colored('12h_ch', 'blue'), colored('30d_ch', 'blue'),
                                     colored('1y_ch', 'magenta'), colored('30m_MA', 'blue'), colored('30d_MA', 'blue'),
                                     colored('Price', 'blue')]
            elif (sort_index % len(toggle_sort) == 6):
                table.field_names = [colored('Symbol', 'blue'), colored('Score', 'blue'), colored('2m_ch', 'blue'),
                                     colored('6h_ch', 'blue'), colored('12h_ch', 'blue'), colored('30d_ch', 'blue'),
                                     colored('1y_ch', 'blue'), colored('30m_MA', 'magenta'), colored('30d_MA', 'blue'),
                                     colored('Price', 'blue')]
            elif (sort_index % len(toggle_sort) == 7):
                table.field_names = [colored('Symbol', 'blue'), colored('Score', 'blue'), colored('2m_ch', 'blue'),
                                     colored('6h_ch', 'blue'), colored('12h_ch', 'blue'), colored('30d_ch', 'blue'),
                                     colored('1y_ch', 'blue'), colored('30m_MA', 'blue'), colored('30d_MA', 'magenta'),
                                     colored('Price', 'blue')]

            for index in range(10):
                i = sorted_data[index]
                table.add_row(
                    [symbols[i], current_score[i], color(change_2m[i]), color(change_6h[i]), color(change_12h[i]),
                     color(change_30d[i]), color(change_1y[i]), color(moving_average_30m[i]),
                     color(moving_average_30d[i]), current_price[i]])
            print(table)
            print('\n')
            sort_index += 1
            count += 1
            time.sleep(5)

    threads = [threading.Thread(target=kline_continuum),
               threading.Thread(target=print_results)]

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
