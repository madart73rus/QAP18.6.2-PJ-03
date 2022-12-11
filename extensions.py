import  json
import requests
from config import keys

class APIException(Exception):
    pass

class СurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base} ')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]*amount

        
        return total_base
