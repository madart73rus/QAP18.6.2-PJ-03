import telebot
from config import keys, TOKEN
from extensions import APIException, СurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])  # обработчик команд  /start или /help
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты>   \
<в какую валюту перевести>   \
<количество переводимой валюты>\n Получить список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])       # обработчик команды  /values
def value(message: telebot.types.Message):
    text = 'Доступные валюты :'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])      # обработчик сообщения пользователя \
        # <имя валюты цену которой он хочет узнать> <имя валюты в которой надо узнать цену первой валюты>\
        # <количество первой валюты>
def convert(message: telebot.types.Message):

    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное число парамметров')

        base, quote, amount = values
        total_base = СurrencyConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote}  -  {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

