from binance import client
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('TkAgg')
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import warnings

warnings.filterwarnings("ignore")

api_key = 'TubOoVOsqYOA53iIOWAcv4b4PXWFOQ8EeIeVnQ4urPdSOrGeT3N8LiWsu6oYT0of'
sec_key = 'prdmbg6Mhr10QgrIAiEAp9lNEnsM92YESjwHtMLysg0X6itfCtWH3swTb60vIBOy'

client = Client(api_key, sec_key)


def predict_FPrice(symbol):
    df = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, start_str="1 year ago UTC")

    df = pd.DataFrame(df, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Volume',
                                   'Trades', 'Buy Base', 'Buy Quote', 'Ign'])

    df['Date'] = pd.to_datetime(df['Date'], unit='ms')

    dataset_train = df
    training_set = dataset_train.iloc[:, 4:5].values

    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)

    X_train = []
    y_train = []
    for i in range(60, len(training_set_scaled)):
        X_train.append(training_set_scaled[i - 60:i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    my_model = Sequential()
    my_model.add(LSTM(units=50, return_sequences=True, activation='relu', input_shape=(X_train.shape[1], 1)))
    my_model.add(Dropout(0.2))
    my_model.add(LSTM(units=50, return_sequences=True))
    my_model.add(Dropout(0.2))
    my_model.add(LSTM(units=50, return_sequences=True))
    my_model.add(Dropout(0.2))
    my_model.add(LSTM(units=50))
    my_model.add(Dropout(0.2))
    my_model.add(Dense(units=1))

    my_model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae', 'mse'])

    my_model.fit(X_train, y_train, epochs=70, batch_size=32, verbose=1)
    my_model.save(symbol + ".h5")

    dataset_total = training_set
    inputs = dataset_total[len(dataset_total) - 90:]
    inputs = inputs.reshape(-1, 1)
    inputs = sc.transform(inputs)

    X_test = []
    for i in range(60, 90):
        X_test.append(inputs[i - 60:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted_crypto_price = my_model.predict(X_test)
    predicted_crypto_price = sc.inverse_transform(predicted_crypto_price)


predict_FPrice("BTCUSDT")
predict_FPrice("ETHUSDT")
predict_FPrice("LTCUSDT")
