import plotly.graph_objects as go
import pandas as pd
from datetime import date
import requests


# Define the API endpoints
def MyFunc5():
    api_candlesticks = 'https://api.binance.com/api/v3/klines?interval=1d&limit=1000&symbol='
    api_symbol_names = 'https://api.binance.com/api/v3/ticker/24hr'

    # Function to plot a candlestick graph for a given symbol name
    def plot_candlestick_graph(symbol):
        # Retrieve the candlestick data from Binance API
        api_url = api_candlesticks + symbol
        response = requests.get(api_url)
        data = response.json()

        # Convert the data to a pandas DataFrame and add a Date column
        df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                         'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                         'Taker Buy Quote Asset Volume', 'Ignore'])
        df['Date'] = pd.to_datetime(df['Open Time'], unit='ms')

        # Create the candlestick chart using Plotly
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'])])
        fig.update_layout(title=symbol + " Crypto (July 2017 - Present Day)", yaxis_title='US DOLLARS($)')
        fig.show()

    # Retrieve the list of symbol names and their trading volumes from Binance API
    response = requests.get(api_symbol_names)
    data = response.json()
    symbols = [item['symbol'] for item in data if float(item['quoteVolume']) >= 100]
    top10 = [item['symbol'] for item in data if float(item['quoteVolume']) >= 100][:10]

    # Show the list of top 10 crypto currencies by trading volume
    print("Top 10 Crypto Currencies by Trading Volume:")
    for i, crypto in enumerate(top10):
        print(f"{i+1}. {crypto}")

    # Get input from the user for three crypto currencies to plot
    crypto_list = []
    for i in range(3):
        crypto = input(f"Enter the number of crypto currency {i+1} to plot (1-10): ")
        if crypto.isdigit() and int(crypto) in range(1, 11):
            crypto_list.append(top10[int(crypto)-1])
        else:
            print("Invalid input. Please try again.")
            return

    # Plot candlestick graphs for each crypto currency in the list
    for crypto in crypto_list:
        plot_candlestick_graph(crypto)
