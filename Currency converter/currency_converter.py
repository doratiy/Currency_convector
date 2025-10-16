import os
import requests
from dotenv import load_dotenv
import argparse
from requests import HTTPError


def get_exchange_rate(api_key, base_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        base_currencies = response.json()["conversion_rates"]
        return base_currencies
    except HTTPError:
        print("непраильно набранна базовая валюта")


def convert_amount(target_currency, amount_of_money, base_currencies):
    if target_currency in base_currencies:
        converted_amount = float(amount_of_money) * float(base_currencies[f"{target_currency}"])
        return converted_amount


if __name__ == "__main__":
    load_dotenv(".env")
    api_key = os.environ["API_KEY"]
    parser = argparse.ArgumentParser(description="конвертирует суммы валют")
    parser.add_argument("-b", "--base", help="Введите код базовой валюты (например, RUB)", required=True)
    parser.add_argument("-t", "--target", help="Введите код целевой валюты (например, USD)", required=True)
    parser.add_argument("-a", "--amount", help="Введите сумму денег:", required=True)
    args = parser.parse_args()
    base_currency = args.base.upper()
    target_currency = args.target.upper()
    amount_of_money = args.amount
    base_currencies = get_exchange_rate(api_key, base_currency)
    converted_amount = convert_amount(target_currency, amount_of_money, base_currencies)
    print("Конвертированная сумма ", converted_amount, target_currency)

