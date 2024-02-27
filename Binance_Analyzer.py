import time
from playsound import playsound
import requests
from termcolor import colored
from prettytable import PrettyTable


def MyFunc7():
    print("\n" * 10)
    api = "https://api.binance.com/api/v3/ticker/24hr"

    api_klines_1m = "https://api.binance.com/api/v3/klines?interval=1m&limit=1000&symbol="  # 1 min interval
    api_klines_15m = "https://api.binance.com/api/v3/klines?interval=15m&limit=1000&symbol="  # 15 min interval

    symbols = []
    indexes = []

    data = requests.get(api).json()

    minimum_volume = 100

    for currency in data:
        if "BTC" in currency['symbol'] and float(currency['quoteVolume']) > minimum_volume:
            symbols.append(currency['symbol'])
            indexes.append(data.index(currency))

    k_line_1m = [[] for each in range(len(symbols))]
    k_line_15m = [[] for each in range(len(symbols))]

    # print(symbols)
    print("Found " + colored(str(len(symbols)), 'green') + " CryptoCurrencies that are worth Investing")
    time.sleep(2)
    print("Getting the Data.....")
    time.sleep(2)
    print("Running Analyzer.....")
    print(" ")

    def kline_calculate(api):
        prices = [[] for each in range(len(symbols))]

        for symbol in symbols:
            temp_api = api_klines_1m + symbol
            candlesticks = requests.get(temp_api).json()
            for candle in candlesticks:
                prices[symbols.index(symbol)].append(float(candle[1]))
        #   print(prices[symbols.index(symbol)])
        return prices

    k_line_1m = kline_calculate(api_klines_1m)
    k_line_15m = kline_calculate(api_klines_15m)

    current_price = [0 for x in range(len(symbols))]
    price_change_2_min = [0 for x in range(len(symbols))]
    price_change_5_min = [0 for x in range(len(symbols))]
    price_change_15_min = [0 for x in range(len(symbols))]
    price_change_30_min = [0 for x in range(len(symbols))]
    # price_change_25_30_min = [0 for x in range(len(symbols))]
    price_change_1_hour = [0 for x in range(len(symbols))]
    price_change_3_hour = [0 for x in range(len(symbols))]
    price_change_8_hour = [0 for x in range(len(symbols))]
    price_change_1_days = [0 for x in range(len(symbols))]
    price_change_3_days = [0 for x in range(len(symbols))]
    price_change_5_days = [0 for x in range(len(symbols))]
    price_change_7_days = [0 for x in range(len(symbols))]
    price_change_10_days = [0 for x in range(len(symbols))]
    average_10_min = [0 for x in range(len(symbols))]
    average_20_min = [0 for x in range(len(symbols))]
    average_50_min = [0 for x in range(len(symbols))]
    average_100_min = [0 for x in range(len(symbols))]
    average_change_10_min = [0 for x in range(len(symbols))]
    average_change_20_min = [0 for x in range(len(symbols))]
    average_change_50_min = [0 for x in range(len(symbols))]
    average_change_100_min = [0 for x in range(len(symbols))]
    total_score = [0 for x in range(len(symbols))]
    ratio5_10sec = [[] for y in range(len(symbols))]
    ratio5_sum_10sec = [[] for y in range(len(symbols))]

    def kline_continuum():
        data = requests.get(api).json()
        i = 0
        for index in indexes:
            current_price[i] = float(data[index]['lastPrice'])
            k_line_1m[i].append(current_price[i])
            i += 1

    def calculate_change(current_price, list, index, number):
        try:
            result = round(current_price * 100 / list[index] - 100, number)
        except:
            return 0

        return result

    def color(nr):
        if nr > 0:
            return ('\033[92m' + str(nr) + '\033[0m')  # Green Color
        else:
            return ('\033[91m' + str(nr) + '\033[0m')  # Red Color

    def calculate_score():
        for x in range(len(symbols)):
            price_change_2_min[x] = calculate_change(current_price[x], k_line_1m[x], -2, 2)
            price_change_5_min[x] = calculate_change(current_price[x], k_line_1m[x], -5, 2)
            price_change_15_min[x] = calculate_change(current_price[x], k_line_1m[x], -15, 2)
            price_change_30_min[x] = calculate_change(current_price[x], k_line_1m[x], -30, 2)
            price_change_1_hour[x] = calculate_change(current_price[x], k_line_1m[x], -60, 2)
            price_change_3_hour[x] = calculate_change(current_price[x], k_line_1m[x], -180, 2)
            price_change_8_hour[x] = calculate_change(current_price[x], k_line_1m[x], 20, 2)

            price_change_1_days[x] = calculate_change(current_price[x], k_line_15m[x], -96, 1)
            price_change_3_days[x] = calculate_change(current_price[x], k_line_15m[x], -288, 1)
            price_change_5_days[x] = calculate_change(current_price[x], k_line_15m[x], -480, 1)
            price_change_7_days[x] = calculate_change(current_price[x], k_line_15m[x], -672, 1)
            price_change_10_days[x] = calculate_change(current_price[x], k_line_15m[x], -960, 1)

            average_10_min[x] = round(float(sum(k_line_1m[x][- 10:])) / 10, 8)
            average_20_min[x] = round(float(sum(k_line_1m[x][- 20:])) / 20, 8)
            average_50_min[x] = round(float(sum(k_line_1m[x][- 50:])) / 50, 8)
            average_100_min[x] = round(float(sum(k_line_1m[x][- 100:])) / 100, 8)

            average_change_10_min[x] = round(float(current_price[x]) * 100 / float(average_10_min[x]) - 100, 2)
            average_change_20_min[x] = round(float(current_price[x]) * 100 / float(average_20_min[x]) - 100, 2)
            average_change_50_min[x] = round(float(current_price[x]) * 100 / float(average_50_min[x]) - 100, 2)
            average_change_100_min[x] = round(float(current_price[x]) * 100 / float(average_100_min[x]) - 100, 2)

        for x in range(len(symbols)):
            score = 0

            # 2 minute change parameter score calculation
            a = float(price_change_2_min[x])
            if a > 0 and a < 0.5:
                score += 1
            elif a >= 0.5 and a < 1:
                score += 1.25
            elif a >= 1 and a < 1.5:
                score += 1.5
            elif a >= 1.5 and a < 2:
                score += 0.5
            elif a >= 3:
                score += 0.25

            # 5 minute change parameter score calculation
            a = float(price_change_5_min[x])
            if a > 0 and a < 0.5:
                score += 1
            elif a >= 0.5 and a < 1:
                score += 1.25
            elif a >= 1 and a < 2:
                score += 1.5
            elif a >= 2 and a < 3:
                score += 0.5
            elif a >= 3:
                score += 0.25

            # 15 minute change parameter score calculation
            a = float(price_change_15_min[x])
            if a <= 1 and a > -0.5:
                score += 0.25
            elif a <= -0.5 and a > -1:
                score += 0.5
            elif a <= -1 and a > -1.5:
                score += 0.75
            elif a <= -1.5:
                score += 1

            # 1 hour change parameter score calculation
            a = float(price_change_1_hour[x])
            if a <= 2 and a >= 0:
                score += 0.5
            elif a <= 0 and a > -2:
                score += 0.75
            elif a <= -2:
                score += 1

            # 3 hour change parameter score calculation
            a = float(price_change_3_hour[x])
            if a <= 5 and a > -1:
                score += 0.25
            elif a <= -1 and a > -3:
                score += 0.5
            elif a <= -3 and a > -6:
                score += 0.75
            elif a <= -6:
                score += 1

            # 8 hour change parameter score calculation
            a = float(price_change_8_hour[x])
            if a <= 0 and a > -4:
                score += 0.25
            elif a <= -4 and a > -6:
                score += 0.5
            elif a <= -6:
                score += 0.75

            a = 0
            for i in range(len(ratio5_10sec[x])):
                if float(price_change_2_min[x]) > 0.55 or float(price_change_5_min[x]) > 1:
                    if float(ratio5_10sec[x][i]) > 0:
                        a += 1
                        if float(ratio5_sum_10sec[x][i]) > 0.3:
                            a += 1
            try:
                score += a / len(ratio5_sum_10sec[x])
            except Exception:
                score += a

            a = 0
            for i in range(len(ratio5_10sec[x]) - 1):
                if float(ratio5_10sec[x][i]) > 0:
                    a += 1
            if a <= 2:
                score += 0.25
            elif a > 2 and a <= 4:
                score += 0.5
            elif a > 4 and a <= 7:
                score += 0.75
            elif a > 7:
                score += 1

            a = 0
            for i in range(20, 1, -1):
                if float(k_line_1m[x][-i]) > float(k_line_1m[x][-(i - 1)]):
                    a += 1
            score += a / 10

            # 1 day change parameter score calculation
            if float(price_change_1_days[x]) > 5:
                score += 0.3
            # 3 day change parameter score calculation
            if float(price_change_3_days[x]) > 10:
                score += 0.25
            # 5 day change parameter score calculation
            if float(price_change_5_days[x]) > 15:
                score += 0.25
            # 7 day change parameter score calculation
            if float(price_change_7_days[x]) > 20:
                score += 0.25
            # 10 day change parameter score calculation
            if float(price_change_10_days[x]) > -25:
                score += 0.25

            # 10 minutes moving average parameter score calculation
            a = float(average_change_10_min[x])
            if a < 0.2 and a > -0.3:
                score += 0.1
            # 20 minutes moving average parameter score calculation
            a = float(average_change_20_min[x])
            if a < 0.2 and a > -0.3:
                score += 0.1
            # 50 minutes moving average parameter score calculation
            a = float(average_change_50_min[x])
            if a < 0.2 and a > -0.3:
                score += 0.1
            # 100 minutes moving average parameter score calculation
            a = float(average_change_100_min[x])
            if a < 0.2 and a > -0.3:
                score += 0.1

            # save score
            total_score[x] = score

    count = 0
    while count < 5:
        kline_continuum()
        calculate_score()
        table = PrettyTable()
        sort_by = total_score

        sorted_data = sorted(range(len(sort_by)), key=lambda k: sort_by[k])
        sorted_data.reverse()

        print(colored(time.ctime(), 'blue'))
        table.field_names = [colored('Symbol', 'magenta'), colored('Score'), colored('2_m_ch', 'magenta'),
                             colored('5_m_ch', 'magenta'), colored('15_m_ch', 'magenta'),
                             colored('30_m_ch', 'magenta'), colored('1_hr_ch', 'magenta'),
                             colored('10_m_MA', 'magenta'), colored('20_m_MA', 'magenta'),
                             colored('50_m_MA', 'magenta'), colored('100_m_MA', 'magenta'),
                             colored('8_hr_ch', 'magenta'), colored('1_day_ch', 'magenta'),
                             colored('3_day_ch', 'magenta'), colored('5_day_ch', 'magenta'),
                             colored('7_day_ch', 'magenta'), colored('10_day_ch', 'magenta')]
        # print top 10 cryptocurrencies data
        for k in range(10):
            i = sorted_data[k]
            table.add_row([symbols[i][:-3], colored(round(total_score[i], 2), 'blue'), color(price_change_2_min[i]),
                           color(price_change_5_min[i]), color(price_change_15_min[i]),
                           color(price_change_30_min[i]),
                           color(price_change_1_hour[i]), color(average_change_10_min[i]),
                           color(average_change_20_min[i]), color(average_change_50_min[i]),
                           color(average_change_100_min[i]), color(price_change_8_hour[i]),
                           color(price_change_1_days[i]), color(price_change_3_days[i]),
                           color(price_change_5_days[i]),
                           color(price_change_7_days[i]), color(price_change_10_days[i])])
        print(table)

        '''try:
            if float(total_score[sorted_data[0]]) > 4.5:
                playsound('Sound.wav')
        except Exception as e:
            print(e)'''

        print('\n')
        count += 1
        time.sleep(1)
