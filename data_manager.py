import requests
import sqlite3
import constants as const
from datetime import datetime, timedelta


def make_request(currency, start_date, end_date):
    result = {}
    if currency not in const.Currency.value2member_map_ \
            or not 0 < (end_date - start_date).days <= const.REQUEST_LIMIT:
        print(f'Invalid argument CURRENCY: {currency}/START-DATE: {start_date}/END-DATE: {end_date}')
    else:
        response = requests.get(
            f'http://api.nbp.pl/api/exchangerates/'
            f'rates/a/{currency}/{start_date.date()}/{end_date.date()}/?format=json')
        if response.status_code != 200:
            print(f'Request Error {response.status_code}')
        else:
            result = response
    return result


def get_range(currency, start_date, end_date):
    if start_date.weekday() >= 5:
        start_date -= timedelta(days=(start_date.weekday() % 4))
    dates = split_date(start_date, end_date)
    x = {
        'rates': []
    }
    for date_range in dates:
        response = make_request(currency, date_range[0], date_range[1])
        if isinstance(response, int) or response is None:
            print(f'Failed fetching data between {date_range[0]} and {date_range[1]}')
        else:
            x['rates'] = x['rates'] + response.json()['rates']
    return fix_response(x)


def get_previous_days(currency, days):
    current_date = datetime.now()
    beginning = current_date - timedelta(days=days)
    return get_range(currency, beginning, current_date)


def fix_response(response):
    x = []
    previous_date = response['rates'][0]
    for value in response['rates']:
        for date in range(1, (to_date(value['effectiveDate']) - to_date(previous_date['effectiveDate'])).days):
            x.append((to_date(previous_date['effectiveDate']) + timedelta(days=date), previous_date['mid']))
        x.append((to_date(value['effectiveDate']), value['mid']))
        previous_date = value
    return x


def to_date(date):
    if isinstance(date, datetime):
        return date
    else:
        return datetime.strptime(date, '%Y-%m-%d')


def split_date(start_date, end_date):
    days_between = (to_date(end_date) - to_date(start_date)).days
    print(f'days between: {days_between}')
    dates = []
    while days_between != 0:
        if days_between >= const.REQUEST_LIMIT:
            dates.append((to_date(end_date) - timedelta(days=days_between), to_date(end_date) -
                          timedelta(days=days_between) + timedelta(days=const.REQUEST_LIMIT - 1)))
            days_between -= const.REQUEST_LIMIT
        else:
            dates.append((to_date(end_date) - timedelta(days=days_between), to_date(end_date)))
            days_between = 0
    return dates


def fill_currency(currency, start_date, end_date):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    print("Opened database successfully")
    safe_date = (to_date(start_date).timestamp(), to_date(end_date).timestamp(), currency)
    query_result = c.execute('''SELECT COUNT(*) FROM currency_stats
     where date between ? and ? and symbol like ? ORDER BY date''', safe_date)
    currency_values = []
    if query_result != (to_date(end_date) - to_date(start_date)).days:
        currency_values = get_range(currency, to_date(start_date), to_date(end_date))
    duplicates = 0
    for daily_value in currency_values:
        safe_data = (currency.upper(), daily_value[0].timestamp(), daily_value[1])
        try:
            c.execute('INSERT INTO currency_stats(symbol,date,value) VALUES(?,?,?)', safe_data)
        except sqlite3.IntegrityError:
            duplicates += 1
    if duplicates != 0:
        print(f'{duplicates} values were not added to database due to Integrity Error')
    conn.commit()
    conn.close()


def get_currency(currency, start_date, end_date):
    if (to_date(end_date) - to_date(start_date)).days < 0:
        print('Illegal argument')
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    print("Opened database successfully")
    x = []
    safe_date = (to_date(start_date).timestamp(), to_date(end_date).timestamp(), currency)
    for row in c.execute('SELECT value, date from currency_stats'
                         ' where date between ? and ? and symbol like ? ORDER BY date', safe_date):
        x.append((datetime.fromtimestamp(int(row[1])).date(), float(row[0])))
    conn.close()
    return x


def get_difference(first_value, second_value):
    return -((first_value - second_value)/first_value) * 100


def get_avg(values):
    return sum([pair[1] for pair in values])/len(values)
