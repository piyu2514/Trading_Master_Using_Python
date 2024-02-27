from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from prettytable import PrettyTable
import json
from termcolor import colored


def MyFunc1():
    # print("\n" * 100)
    listings_api = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '8da10793-c1e9-4dce-8917-91b573eb0560',
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(listings_api, params=parameters)
        listings_data = json.loads(response.text)['data']
        # print(*listings_data,sep='\n')
    except(ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    table = PrettyTable()

    table.field_names = ['Name', 'Symbol', 'Price', 'Volume', 'MarketCap', 'Change 1h', 'Change 24h', 'Change 7d']
    coins = []

    def isNone(number):
        if number:
            n = "{:.6f}".format(number)
            return float(n)
        return 0

    def color(nr):
        if nr > 0:
            return ('\033[92m' + str(nr) + '\033[0m')  # Green Color
        else:
            return ('\033[91m' + str(nr) + '\033[0m')  # Red Color

    for coin in listings_data:
        name = coin['name']
        symbol = coin['symbol']
        coin_data = coin['quote']['USD']

        coins.append([name,  # coins[0]
                      symbol,  # coins[1]
                      isNone(coin_data['price']),  # coins[2]
                      isNone(coin_data['volume_24h']),  # coins[3]
                      isNone(coin_data['market_cap']),  # coins[4]
                      color(isNone(coin_data['percent_change_1h'])),  # coins[5]
                      color(isNone(coin_data['percent_change_24h'])),  # coins[6]
                      color(isNone(coin_data['percent_change_7d']))])  # coins[7]

    '''
    table.sortby = 'Change 24h'
    table.reversesort = True
    print(table)
    '''

    # print(*coins, sep='\n')
    i = 1
    while True:
        number = 1
        print("Press:")
        '''
            for item in table.field_names:
                print(str(number) + '. Sort by ' + item)
                number += 1
            '''
        print("1. Sort by " + colored("Name", 'cyan') + " of the CryptoCurrency")
        print("2. Sort by " + colored("Symbol", 'cyan') + " of the CryptoCurrency")
        print("3. Rank by " + colored("Price", 'cyan') + " of the CryptoCurrency")
        print("4. Rank by " + colored("Volume", 'cyan') + " of the CryptoCurrency")
        print("5. Rank by " + colored("MarketCap", 'cyan') + " of the CryptoCurrency")
        print("6. Rank by " + colored("Change in the last 1 hour", 'cyan'))
        print("7. Rank by " + colored("Change in the last 24 hours", 'cyan'))
        print("8. Rank by " + colored("change in the last 7 days", 'cyan'))
        print("")
        choice = input("Choose option: ")
        choice = int(choice)
        print("")
        if choice == 1:
            coins.sort(key=lambda x: x[choice - 1])
            coins.reverse()
            [table.add_row(coin) for coin in coins[:100]]  # 100 sorted
            print(table)

        elif choice == 2:
            coins.sort(key=lambda x: x[choice - 1])
            coins.reverse()
            [table.add_row(coin) for coin in coins[:100]]
            print(table)

        elif choice == 3:
            coins.sort(key=lambda x: x[choice - 1])
            coins.reverse()
            [table.add_row(coin) for coin in coins[:100]]
            print(table)
            print()
            print("The " + colored("MOST EXPENSIVE", 'blue') + " CryptoCurrency right now :")
            print(table[:1])
            print()
            print("The " + colored("LEAST EXPENSIVE", 'blue') + " CryptoCurrency right now :")
            print(table.get_string(start=99))

        elif choice == 4:
            coins.sort(key=lambda x: x[choice - 1])
            coins.reverse()
            [table.add_row(coin) for coin in coins[:100]]
            print(table)
            print()
            print(colored("MAXIMUM TRADED ", 'blue') + "CryptoCurrency in the last 24 hours :")
            print(table[:1])
            print()
            print(colored("LEAST TRADED ", 'blue') + "CryptoCurrency in the last 24 hours :")
            print(table.get_string(start=99))

        elif choice == 5:
            coins.sort(key=lambda x: x[choice - 1])
            coins.reverse()
            [table.add_row(coin) for coin in coins[:100]]
            print(table)
            print()
            print("CryptoCurrency with the " + colored("MAXIMUM CAPITALIZATION :", 'blue'))
            print(table[:1])
            print()
            print("CryptoCurrency with the " + colored("LEAST CAPITALIZATION :", 'blue'))
            print(table.get_string(start=99))

        elif choice == 6:
            coins.sort(key=lambda x: x[choice - 1])
            coins.reverse()
            [table.add_row(coin) for coin in coins[:100]]
            print(table)
            print()
            print("CryptoCurrency that " + colored("Changed the MOST in the last 1 HOUR :", 'blue'))
            print(table[:1])
            print()
            print("CryptoCurrency that " + colored("Changed the LEAST in the last 1 HOUR :", 'blue'))
            print(table.get_string(start=99))

        elif choice == 7:
            coins.sort(key=lambda x: x[choice - 1])
            coins.reverse()
            [table.add_row(coin) for coin in coins[:100]]
            print(table)
            print()
            print("CryptoCurrency that " + colored("Changed the MOST in the last 24 HOURS :", 'blue'))
            print(table[:1])
            print()
            print("CryptoCurrency that " + colored("Changed the LEAST in the last 24 HOURS :", 'blue'))
            print(table.get_string(start=99))

        elif choice == 8:
            coins.sort(key=lambda x: x[choice - 1])
            coins.reverse()
            [table.add_row(coin) for coin in coins[:100]]
            print(table)
            print()
            print("CryptoCurrency that " + colored("Changed the MOST in the last 7 DAYS :", 'blue'))
            print(table[:1])
            print()
            print("CryptoCurrency that " + colored("Changed the LEAST in the last 7 DAYS :", 'blue'))
            print(table.get_string(start=99))

        print()
        table.clear_rows()
        print("Do you want to continue ?")
        ch = input()
        if (ch == 'yes' or ch == 'Yes' or ch == 'YES' or ch == 'y' or ch == 'Y'):
            i = i + 1
            continue
        else:
            print("Thank You !!")
            break


