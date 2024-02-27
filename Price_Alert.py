import pandas as pd
import json
from requests import Session
import time
import pyttsx3
from termcolor import colored
from twilio.rest import Client


def MyFunc3():
    print("\n" * 10)
    engine = pyttsx3.init()

    df = pd.read_csv('Coins.csv', usecols=['Symbol', 'Up', 'Down'])
    df = df.to_json()
    df = json.loads(df)

    symbols = df['Symbol']
    Up_limits = df['Up']
    Down_limits = df['Down']

    symbols = [symbols[x] for x in symbols]
    Up_limits = [float(Up_limits[x]) for x in Up_limits]
    Down_limits = [float(Down_limits[x]) for x in Down_limits]

    '''
    print(symbols)
    print(Up_limits)
    print(Down_limits)
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

    def printing():
        while True:
            current_price = get_latest_data()
            for index in range(len(symbols)):
                current_price[index] = round(current_price[index], 6)
                if current_price[index] > Up_limits[index]:
                    print(colored(symbols[index], 'blue') + " price " + colored("WENT UP",
                                                                                'green') + ". Current Price is "
                                                                                           "$ " + colored(
                        current_price[index], 'green'))
                    speak(str(symbols[index]) + " price WENT UP. Current Price is " + str(
                        current_price[index]) + "dollars")
                    '''send_whatsapp(str(symbols[index].upper()) + " price WENT UP.\nCurrent Price : $ " + str(
                        current_price[index]))'''

                if current_price[index] < Down_limits[index]:
                    print(colored(symbols[index], 'blue') + " price " + colored("DROPPED",
                                                                                'red') + ". Current Price is $ "
                          + colored(current_price[index], 'red'))
                    speak(str(symbols[index]) + " price DROPPED. Current Price is " + str(
                        current_price[index]) + "dollars")
                    '''send_whatsapp(str(symbols[index].upper()) + " price DROPPED.\nCurrent Price : $ " + str(
                        current_price[index]))'''

            '''send_whatsapp("Price Alerts will continue after 1 minute.")'''
            time.sleep(60)  # Refresh after 60 seconds

    '''def send_whatsapp(message):
        account_sid = "AC0eb07259a1278eb10b32cdaf6db436c0"
        #account_sid ='MG5e43395fb7f3a42773da73e20e870ff6'
        auth_token = "8af0da3523fc56308a12e2a50d6caff9"

        client = Client(account_sid, auth_token)

        from_whatsapp_number = 'whatsapp:+13465454944'
        to_whatsapp_number = 'whatsapp:+918950882340'

        client.messages.create(body=message,
                               from_=from_whatsapp_number,
                               to=to_whatsapp_number)'''

    def get_latest_data():
        session = Session()
        session.headers.update(headers)

        current_price = [0 for x in range(len(symbols))]

        response = session.get(api, params=p1)
        data = json.loads(response.text)['data']
        current_price[0] = float(data['1']['quote']['USD']['price'])

        response = session.get(api, params=p2)
        data = json.loads(response.text)['data']
        current_price[1] = float(data['1376']['quote']['USD']['price'])

        response = session.get(api, params=p3)
        data = json.loads(response.text)['data']
        current_price[2] = float(data['463']['quote']['USD']['price'])

        response = session.get(api, params=p4)
        data = json.loads(response.text)['data']
        current_price[3] = float(data['1787']['quote']['USD']['price'])

        response = session.get(api, params=p5)
        data = json.loads(response.text)['data']
        current_price[4] = float(data['3252']['quote']['USD']['price'])

        response = session.get(api, params=p6)
        data = json.loads(response.text)['data']
        current_price[5] = float(data['5028']['quote']['USD']['price'])

        return current_price

    # print(current_price)  # List of current prices of all 6 from api

    def speak(message):
        engine.say(message)
        engine.runAndWait()

    printing()


