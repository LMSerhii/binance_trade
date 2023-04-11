import time

import talib
from telebot import TeleBot, types
import webbrowser

from trade_bot import TradeBot
from auth_telegram import token

bot = TeleBot(token=token)


@bot.message_handler(commands=['start'])
def greetings(message):
    bot.send_message(
        message.chat.id,
        f'<b>Привет</b>,    <em>{message.from_user.first_name} {message.from_user.last_name}</em>',
        # message,
        parse_mode='html'
    )


@bot.message_handler(commands=['start_robot'])
def start_alert(message):
    cfx = TradeBot(symbol=SYMBOL)
    buy = False
    sell = True
    while True:
        closing_data = cfx.get_data()
        rsi = talib.RSI(closing_data, 7)[-1]
        print(rsi)
        if rsi <= 30 and sell:
            # print(f"BUY!!!!")
            bot.send_message(message.chat.id, 'BUY!!! BUY!!! BUY!!!')
            buy = not buy
            sell = not sell
        if rsi >= 70 and buy:
            # print("SELL!!!")
            bot.send_message(message.chat.id, "SELL!!! SELL!!! SELL!!!")
            buy = not buy
            sell = not sell
        time.sleep(2)


if __name__ == '__main__':
    bot.polling(none_stop=True)
