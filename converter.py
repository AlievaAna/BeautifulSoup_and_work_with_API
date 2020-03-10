from bs4 import BeautifulSoup
from decimal import Decimal

def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp?date_req={}".format(date))
    soup = BeautifulSoup(response.content, 'xml')
    if cur_from == 'RUR':
        value_from_RUB = amount
    else:
        valute_from = soup.find('CharCode', text=cur_from).find_parent()
        value_from_RUB = Decimal(amount * Decimal(valute_from.Value.string.replace(',', '.')) / Decimal(valute_from.Nominal.string))
    valute_to = soup.find('CharCode', text=cur_to).find_parent()
    value_to_RUB = Decimal(value_from_RUB * Decimal(valute_to.Nominal.string) / Decimal(valute_to.Value.string.replace(',', '.')))
    
    return Decimal(value_to_RUB).quantize(Decimal("1.0000"))