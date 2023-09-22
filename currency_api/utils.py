import requests
from .models import Currency
from datetime import datetime

def update_exchange_rates():
    # Отримати курси валют з Freecurrencyapi за допомогою API ключа
    api_key = 'fca_live_FdA8LzborXHs2342ZAFdAwuwc5QCdoYqpa8lP5WG'
    base_url = 'https://api.freecurrencyapi.com/v1/latest'

    params = {'apikey': api_key}
    response = requests.get(base_url, params=params) 

    if response.status_code == 200:
        data = response.json()
        rates = data.get('data', {})
        print(rates)

        # Оновити курси валют у базі даних
        for currency_code, exchange_rate in rates.items():
            currency, created = Currency.objects.get_or_create(currency_code=currency_code)
            currency.exchange_rate = exchange_rate
            currency.last_updated = datetime.now()
            currency.save()

        return True
    else:
        return False