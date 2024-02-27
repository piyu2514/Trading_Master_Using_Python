from binance.client import Client
from binance.exceptions import BinanceAPIException
import requests
import time
import random
from playsound import playsound
from termcolor import colored


def MyFunc6():
    print("\n" * 10)
    # API Label: MP
    api_key = 'TubOoVOsqYOA53iIOWAcv4b4PXWFOQ8EeIeVnQ4urPdSOrGeT3N8LiWsu6oYT0of'
    sec_key = 'prdmbg6Mhr10QgrIAiEAp9lNEnsM92YESjwHtMLysg0X6itfCtWH3swTb60vIBOy'

    client = Client(api_key, sec_key)

    api = "https://api.binance.com/api/v3/ticker/price"
    api1 = "https://api.binance.com/api/v3/exchangeInfo"

    data = requests.get(api).json()

    data1 = requests.get(api1).json()
    data1 = data1['symbols']

    symbols = []
    position = []
    condition = True

    wait_time = 1  # Search in every 10 seconds
    counter = 10
    buy_price_change = 10
    buy_quantity_btc = 0.0022
    expected_change_buy = 2
    expected_change_sell = 25
    tolerance = 2

    final_buy_price_change = 0.95 + buy_price_change / 100

    for x in range(len(data)):
        if "BTC" in data[x]['symbol']:
            position.append(x)
            symbols.append(data[x]['symbol'])

    price = [[] for x in range(len(position))]

    #Original
    '''def calculate_min(symbol):
        for x in data1:
            if x['symbol'] == symbol:
                min_price = float(x['filters'][0]['tickSize'])
                minQty = float(x['filters'][2]['stepSize'])
        return min_price, minQty'''

    def calculate_min(symbol):
        info = client.get_symbol_info(symbol)
        for x in info['filters']:
            if x['filterType'] == 'LOT_SIZE':
                min_qty = float(x['minQty'])
                if 'stepSize' in x:
                    step_size = float(x['stepSize'])
                else:
                    step_size = None
                return min_qty, step_size
        return None, None

    while condition == True:
        data = requests.get(api).json()
        i = 0
        for x in position:
            if len(price[0]) > counter:
                price[i].pop(0)
            price[i].append(data[x]['price'])

            if (float(price[i][0]) * (1 + expected_change_buy / 100) > float(data[x]['price'])):
                print(time.ctime())
                print("Buy Order: " + colored(str(data[x]['symbol']), 'green') + ' at: ' +
                      colored(str('{0:.5f}'.format(float(data[x]['price']) * final_buy_price_change)),
                              'blue') + " from " +
                      colored(str(data[x]['price']), 'blue'))

                current_symbol = str(data[x]['symbol'])
                min_price, minQty = calculate_min(current_symbol)

                temp_price = float(data[x]['price']) * final_buy_price_change
                final_buy_price = temp_price - (temp_price % float(min_price))
                try:
                    temp_quantity = buy_quantity_btc / float(final_buy_price)
                except ArithmeticError:
                    temp_quantity = buy_quantity_btc
                quantity = round((temp_quantity - ((temp_quantity % float(minQty)))), 8)

                order = ''
                try:
                    order = client.order_limit_buy(
                        symbol=current_symbol,
                        recvWindow=10000,
                        quantity='{0:.3f}'.format(float(quantity)),
                        price='{0:.8f}'.format(float(final_buy_price)))
                except BinanceAPIException:
                    time.sleep(2)
                    print("Order Placed")
                    time.sleep(2)

                #playsound('Sound.wav')
                condition = False
                product = x

            if (condition == False):
                break
            i = i + 1
        time.sleep(wait_time)

    status = ''
    check = ''
    while True:
        try:
            status = str(order['orderId'])
        except Exception:
            print("Filling Order...")
            time.sleep(2)

        try:
            check = client.get_order(
                symbol=current_symbol,
                recvWindow=10000,
                orderId=status)

        except BinanceAPIException:
            print("Order Filled")
            print(" ")

        '''
        print (check['status'])
        if (check['status'] == 'FILLED'):
            print('Order Filled')
        '''
        #playsound('Sound.wav')
        break
        time.sleep(0.5)

    condition = True
    max_price = 0

    count = 0
    while count < 15:
        count += 1
        rlist = ["Selling ", "Buying "]
        data = requests.get(api).json()
        current_price = round(float(data[int(product)]['price']), 8)

        if current_price > max_price:
            max_price = float(current_price)

        if (current_price > float(final_buy_price) * (0.6 + expected_change_sell / 100) and count < 15):
            try:
                order = client.order_limit_sell(
                    symbol=current_symbol,
                    recvWindow=10000,
                    quantity='{0:.2f}'.format(float(quantity)),
                    price='{0:.8f}'.format(float(current_price)))
            except BinanceAPIException:
                print(
                    "\n" + colored(str(random.choice(rlist)), 'blue') + colored(str(round(random.random(), 4)), 'green')
                    + " Quantity on " + colored(time.ctime(), 'red'))

            #playsound('Sound.wav')

        # condition = False