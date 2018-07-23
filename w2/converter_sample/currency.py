from bs4 import BeautifulSoup
from decimal import Decimal

URL = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get("{}{}".format(URL, date)).text
    soup = BeautifulSoup(response, "lxml")
    valcurs = soup.find("valcurs")
    api_data = []

    for valute in valcurs.find_all('valute'):
        charcode = valute.find_next('charcode').text
        value = Decimal(valute.find_next('value').text.replace(",", "."))
        nominal = int(valute.find_next('nominal').text)

        api_data.append({
            'charcode': charcode,
            'value': value,
            'nominal': nominal
        })

    cto = {}
    for cur in api_data:
        if cur['charcode'] == cur_to:
            cto = cur
            if cur_from == 'RUR':
                return (Decimal(amount) * cto['nominal'] / Decimal(cto['value'])).quantize(Decimal('.0001'))

    for cur in api_data:
        if cur['charcode'] == cur_from:
            rur = Decimal(amount) * Decimal(cur['value']) / cur['nominal']
            return (rur * cto['nominal'] / Decimal(cto['value'])).quantize(Decimal('.0001'))
