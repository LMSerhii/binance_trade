import time

import numpy as np
import requests
import talib

from binance.client import Client

from config_binance_api import Secret_Key, API_Key


class TradeBot:
    __api_secret = Secret_Key
    __api_key = API_Key

    def __init__(self, symbol='BTCUSDT', interval='15m', limit='200', quant=35):
        """
        :param symbol: название монеты
        :param interval: указание интервала
        :param limit: лимит свечей
        :param quant: количество монет
        """
        client = Client(api_key=API_Key, api_secret=Secret_Key)
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.quant = quant
        self.client = client

    def get_data(self):
        url = f'https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval={self.interval}&limit={self.limit}'
        res = requests.get(url)
        return_data = []
        for each in res.json():
            return_data.append(float(each[4]))

        return np.array(return_data)

    def create_my_order(self, order_type):
        order = self.client.create_order(
            symbol=self.symbol,
            side=order_type,
            type='MARKET',
            quantity=self.quant
        )
        return order

    def place_order(self, order_type):
        if order_type == 'BUY':
            return f'Покупка: {self.create_my_order(order_type=order_type)}'

        if order_type == 'SELL':
            return f'Продажа: {self.create_my_order(order_type=order_type)}'

    def start_alert_bot(self):
        """
        Запускает бота только на оповещение
        :return: string
        """
        while True:
            closing_data = self.get_data()
            rsi = talib.RSI(closing_data, 7)[-1]
            print(rsi)

            if rsi <= 30:
                print(f"BUY!!!!")

            if rsi >= 70:
                print("SELL!!!!")
            time.sleep(2)

    def start_bot(self):
        """
        Запускает бота на открытие позиции
        :return:
        """
        buy = False
        sell = True
        while True:
            closing_data = self.get_data()
            rsi = talib.RSI(closing_data, 7)[-1]
            print(rsi)

            if rsi <= 30 and not buy:
                self.place_order(order_type='BUY')
                print("BUY!!!!")
                buy = not buy
                sell = not sell

            if rsi >= 70 and not sell:
                self.place_order(order_type='SELL')
                print("SELL!!!!")
                buy = not buy
                sell = not sell
            time.sleep(2)




