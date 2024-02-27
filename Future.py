from keras.models import load_model
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from binance.client import Client
from termcolor import colored
import warnings
from datetime import date, datetime, timedelta
from prettytable import PrettyTable
import time
import requests


def MyFunc8():
    print("\n" * 10)
    warnings.filterwarnings("ignore")

    new_model_btc = load_model('BTCUSDT.h5')
    new_model_eth = load_model('ETHUSDT.h5')
    new_model_ltc = load_model('LTCUSDT.h5')

    api_key = 'TubOoVOsqYOA53iIOWAcv4b4PXWFOQ8EeIeVnQ4urPdSOrGeT3N8LiWsu6oYT0of'
    sec_key = 'prdmbg6Mhr10QgrIAiEAp9lNEnsM92YESjwHtMLysg0X6itfCtWH3swTb60vIBOy'

    client = Client(api_key, sec_key)

    api_prev30days = "https://api.binance.com/api/v3/klines?interval=1d&limit=32&symbol="

    sc = MinMaxScaler(feature_range=(0, 1))

    def predict(symbol, current_model):
        df = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY,
                                          start_str="1 year ago UTC")

        df = pd.DataFrame(df, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Volume',
                                       'Trades', 'Buy Base', 'Buy Quote', 'Ign'])

        df['Date'] = pd.to_datetime(df['Date'], unit='ms')

        dataset_train = df
        training_set = dataset_train.iloc[:, 4:5].values

        training_set_scaled = sc.fit_transform(training_set)

        X_train = []
        y_train = []
        for i in range(60, len(training_set_scaled)):
            X_train.append(training_set_scaled[i - 60:i, 0])
            y_train.append(training_set_scaled[i, 0])
        X_train, y_train = np.array(X_train), np.array(y_train)

        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

        current_model.fit(X_train, y_train, epochs=0, batch_size=32, verbose=1)
        dataset_total = training_set
        inputs = dataset_total[len(dataset_total) - 90:]
        inputs = inputs.reshape(-1, 1)
        inputs = sc.transform(inputs)

        X_test = []
        for i in range(60, 90):
            X_test.append(inputs[i - 60:i, 0])
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        predicted_crypto_price = current_model.predict(X_test)
        predicted_crypto_price = sc.inverse_transform(predicted_crypto_price)
        predicted_crypto_price = np.array(predicted_crypto_price)
        newarr = predicted_crypto_price.reshape(-1)
        return newarr

    # 30 days future prediction:
    values_BTCUSDT = predict("BTCUSDT", new_model_btc)
    values_ETHUSDT = predict("ETHUSDT", new_model_eth)
    values_LTCUSDT = predict("LTCUSDT", new_model_ltc)

    # print(values_BTCUSDT)
    # print(values_ETHUSDT)
    # print(values_LTCUSDT)

    # print(values_BTCUSDT[0])

    def color(val, curval):
        if val > curval:
            return ('\033[92m' + str(val) + '\033[0m')  # Green Color
        else:
            return ('\033[91m' + str(val) + '\033[0m')  # Red Color

    def get_prev_data(api, symbol):
        temp_api = api + symbol
        r = requests.get(temp_api)
        r = r.json()

        df = pd.DataFrame.from_records(r)
        df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Volume',
                      'No. of Trades',
                      'Base Asset Volume', 'Quote Asset Volume', 'Ign']

        end_date = date.today()
        data = pd.date_range(end=end_date, periods=len(df), freq='1D')
        df.insert(0, 'Date', data)
        df.drop(['Open Time', 'Open', 'High', 'Low', 'Volume', 'Close Time', 'Quote Volume', 'No. of Trades',
                 'Base Asset Volume', 'Quote Asset Volume', 'Ign'], axis=1, inplace=True)
        # print(df)
        prev_val_30d = round(float(df['Close'].values[1]), 4)
        prev_val_20d = round(float(df['Close'].values[11]), 4)
        prev_val_15d = round(float(df['Close'].values[16]), 4)
        prev_val_10d = round(float(df['Close'].values[21]), 4)
        prev_val_1d = round(float(df['Close'].values[30]), 4)
        current_price = round(float(df['Close'].values[31]), 4)

        return prev_val_1d, prev_val_10d, prev_val_15d, prev_val_20d, prev_val_30d, current_price

    def print_output():
        i = 1
        while True:
            prev_table = PrettyTable()
            print("")
            print("")
            print(colored("                                     CRYPTO-CURRENCIES AVAILABLE FOR TRADING:", 'magenta'))
            print("")
            print(
                "                                             1. " + colored("BITCOIN ", 'blue') + colored("(BTCUSDT)",
                                                                                                           'green'))
            print("")
            print(
                "                                             2. " + colored("ETHEREUM ", 'blue') + colored("(ETHUSDT)",
                                                                                                            'green'))
            print("")
            print(
                "                                             3. " + colored("LITECOIN ", 'blue') + colored("(LTCUSDT)",
                                                                                                            'green'))
            print("")

            symbol = input("Enter the symbol of Crypto-Currency for Trading:")
            symbol = symbol.upper()
            if (symbol == 'BTCUSDT'):
                name = 'BITCOIN'
            elif (symbol == 'ETHUSDT'):
                name = 'ETHEREUM'
            elif (symbol == 'LTCUSDT'):
                name = 'LITECOIN'
            print("")
            print("Getting the Data for " + colored(symbol, 'green') + " ...............")
            print("")
            prev_val_1d, prev_val_10d, prev_val_15d, prev_val_20d, prev_val_30d, current_price = get_prev_data(
                api_prev30days,
                symbol)
            prev_table.field_names = ['Symbol', 'Price 1 Day Ago', 'Price 10 Days Ago', 'Price 15 Days Ago',
                                      'Price 20 Days Ago', 'Price 30 Days Ago']

            prev_val_1d = color(prev_val_1d, current_price)
            prev_val_10d = color(prev_val_10d, current_price)
            prev_val_15d = color(prev_val_15d, current_price)
            prev_val_20d = color(prev_val_20d, current_price)
            prev_val_30d = color(prev_val_30d, current_price)
            d1 = (datetime.now() + timedelta(days=-1)).strftime("%d/%m/%Y")
            d2 = (datetime.now() + timedelta(days=-10)).strftime("%d/%m/%Y")
            d3 = (datetime.now() + timedelta(days=-15)).strftime("%d/%m/%Y")
            d4 = (datetime.now() + timedelta(days=-20)).strftime("%d/%m/%Y")
            d5 = (datetime.now() + timedelta(days=-30)).strftime("%d/%m/%Y")
            prev_table.add_row([" ", d1, d2, d3, d4, d5])
            prev_table.add_row([" ", " ", " ", " ", " ", " "])
            prev_table.add_row([symbol, prev_val_1d, prev_val_10d, prev_val_15d, prev_val_20d, prev_val_30d])
            print("                                         HISTORY OF " + colored(name, 'green') + " ($)")
            print(prev_table)
            print("")
            print("Current Price: " + colored('$ ', 'blue') + colored(str(current_price), 'blue'))
            print("")
            print("Enter the Amount of " + colored(name, 'green') + " :")
            quantity = float(input())
            current_value = current_price * quantity
            print("")
            print("Current Value: " + colored('$ ', 'blue') + colored(str(current_value), 'blue'))
            print("")
            time.sleep(3)
            print("Predicting the Future Value of " + colored(name, 'green') + " ................")
            time.sleep(3)
            print("Fetching Results ..............")
            time.sleep(3)
            print("")
            print_futTable(symbol, current_value, quantity, name)
            print("")
            print("Do you want to check other Crypto-Currencies ?")
            choice = input()
            if (choice == 'yes' or choice == 'Yes' or choice == 'YES' or choice == 'y' or choice == 'Y'):
                i = i + 1
                continue
            else:
                print("Thank You !!")
                break

    def print_futTable(symbol, current_value, quantity, name):
        fut_table = PrettyTable()
        fut_table.field_names = ['Date', 'Duration', 'Predicted Price', 'Profit/Loss', 'Profit/Loss %',
                                 'Predicted Value']
        d1 = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        d10 = (datetime.now() + timedelta(days=10)).strftime("%d/%m/%Y")
        d15 = (datetime.now() + timedelta(days=15)).strftime("%d/%m/%Y")
        d20 = (datetime.now() + timedelta(days=20)).strftime("%d/%m/%Y")
        d30 = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
        dur1 = "After 1 Day"
        dur10 = "After 10 Days"
        dur15 = "After 15 Days"
        dur20 = "After 20 Days"
        dur30 = "After 30 Days"
        print("              Future Predictions for your Investment in " + colored(name, 'green'))
        if (symbol == "BTCUSDT"):
            s1, per1, f1 = calculate_profitloss(current_value, quantity, values_BTCUSDT[0])
            s2, per2, f2 = calculate_profitloss(current_value, quantity, values_BTCUSDT[9])
            s3, per3, f3 = calculate_profitloss(current_value, quantity, values_BTCUSDT[14])
            s4, per4, f4 = calculate_profitloss(current_value, quantity, values_BTCUSDT[19])
            s5, per5, f5 = calculate_profitloss(current_value, quantity, values_BTCUSDT[29])
            fut_table.add_row([d1, dur1, round(values_BTCUSDT[0], 3), s1, per1, f1])
            fut_table.add_row([d10, dur10, round(values_BTCUSDT[9], 3), s2, per2, f2])
            fut_table.add_row([d15, dur15, round(values_BTCUSDT[14], 3), s3, per3, f3])
            fut_table.add_row([d20, dur20, round(values_BTCUSDT[19], 3), s4, per4, f4])
            fut_table.add_row([d30, dur30, round(values_BTCUSDT[29], 3), s5, per5, f5])
            print(fut_table)
        elif (symbol == "ETHUSDT"):
            s1, per1, f1 = calculate_profitloss(current_value, quantity, values_ETHUSDT[0])
            s2, per2, f2 = calculate_profitloss(current_value, quantity, values_ETHUSDT[9])
            s3, per3, f3 = calculate_profitloss(current_value, quantity, values_ETHUSDT[14])
            s4, per4, f4 = calculate_profitloss(current_value, quantity, values_ETHUSDT[19])
            s5, per5, f5 = calculate_profitloss(current_value, quantity, values_ETHUSDT[29])
            fut_table.add_row([d1, dur1, round(values_ETHUSDT[0], 3), s1, per1, f1])
            fut_table.add_row([d10, dur10, round(values_ETHUSDT[9], 3), s2, per2, f2])
            fut_table.add_row([d15, dur15, round(values_ETHUSDT[14], 3), s3, per3, f3])
            fut_table.add_row([d20, dur20, round(values_ETHUSDT[19], 3), s4, per4, f4])
            fut_table.add_row([d30, dur30, round(values_ETHUSDT[29], 3), s5, per5, f5])
            print(fut_table)
        elif (symbol == "LTCUSDT"):
            s1, per1, f1 = calculate_profitloss(current_value, quantity, values_LTCUSDT[0])
            s2, per2, f2 = calculate_profitloss(current_value, quantity, values_LTCUSDT[9])
            s3, per3, f3 = calculate_profitloss(current_value, quantity, values_LTCUSDT[14])
            s4, per4, f4 = calculate_profitloss(current_value, quantity, values_LTCUSDT[19])
            s5, per5, f5 = calculate_profitloss(current_value, quantity, values_LTCUSDT[29])
            fut_table.add_row([d1, dur1, round(values_LTCUSDT[0], 3), s1, per1, f1])
            fut_table.add_row([d10, dur10, round(values_LTCUSDT[9], 3), s2, per2, f2])
            fut_table.add_row([d15, dur15, round(values_LTCUSDT[14], 3), s3, per3, f3])
            fut_table.add_row([d20, dur20, round(values_LTCUSDT[19], 3), s4, per4, f4])
            fut_table.add_row([d30, dur30, round(values_LTCUSDT[29], 3), s5, per5, f5])
            print(fut_table)

    def calculate_profitloss(current_value, quantity, pred_price):
        future_value = float(pred_price) * quantity
        if (future_value >= current_value):
            status = '\033[92m' + 'Profit' + '\033[0m'
            s = future_value - current_value
            percentage = round((s / current_value) * 100, 2)
            percentage = '\033[92m' + str(percentage) + '\033[0m'
            future_value = round(future_value, 3)
            future_value = '\033[92m' + str(future_value) + '\033[0m'
        elif (current_value > future_value):
            status = '\033[91m' + 'Loss' + '\033[0m'
            s = current_value - future_value
            percentage = round((s / current_value) * 100, 2)
            percentage = '\033[91m' + str(percentage) + '\033[0m'
            future_value = round(future_value, 3)
            future_value = '\033[91m' + str(future_value) + '\033[0m'

        return status, percentage, future_value

    print_output()
