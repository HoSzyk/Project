import requests
import sqlite3
import constants as const
from datetime import datetime, timedelta
# import matplotlib
# from draw_figure import *
#
# from tkinter import *
#
# matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
    dates = split_date(start_date, end_date)
    x = []
    for date_range in dates:
        response = make_request(currency, date_range[0], date_range[1])
        if isinstance(response, int) or response is None:
            print(f'Failed fetching data between {date_range[0]} and {date_range[1]}')
        else:
            x = fix_response(response)

    return x


def get_previous_days(currency, days):
    current_date = datetime.now()
    beginning = current_date - timedelta(days=days)
    if beginning.weekday() >= 5:
        beginning -= timedelta(days=(beginning.weekday() % 4))
    return get_range(currency, beginning, current_date)


def fix_response(response):
    x = []
    previous_date = response.json()['rates'][0]
    for value in response.json()['rates']:
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


def fill_currency(currencies, start_date, end_date):
    for currency in currencies:
        currency_values = get_range(currency, start_date, end_date)
        conn = sqlite3.connect('sales.db')
        c = conn.cursor()
        print("Opened database successfully")
        duplicates = 0
        for daily_value in currency_values:
            try:
                safe_data = (currency.upper(), daily_value[0].date(), daily_value[1],)
                c.execute('INSERT INTO sales_currency(symbol,date,value) VALUES(?,?,?)', safe_data)
            except sqlite3.IntegrityError:
                duplicates += 1

        if duplicates != 0:
            print(f'{duplicates} values were not added to database due to Integrity Error')
        conn.commit()
        conn.close()


def split_date(start_date, end_date):
    days_between = (to_date(end_date) - to_date(start_date)).days
    print(days_between)
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


def get_currency(start_date, end_date):
    if (to_date(end_date) - to_date(start_date)).days < 0:
        print('Illegal argument')
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    print("Opened database successfully")
    x = {}

    safe_date = (to_date(start_date).timestamp(), to_date(end_date).timestamp(),)
    for row in c.execute('SELECT value, date from currency where date between ? and ? ORDER BY date', safe_date):
        x[datetime.fromtimestamp(int(row[1])).date()] = float(row[0])
    conn.close()
    return x


# class mclass:
#     def __init__(self, window):
#         self.window = window
#         self.box = Entry(window)
#         self.button = Button(window, text="check", command=self.plot)
#         self.box.pack()
#         self.button.pack()
#         self.fig = create_subplot()
#
#     def plot(self):
#         create_currency_chart(['USD', 'EUR'], 100, self.fig)
#         canvas = FigureCanvasTkAgg(self.fig, master=self.window)
#         canvas.get_tk_widget().pack()
#         canvas.draw()
#
#
# if __name__ == '__main__':
#     window = Tk()
#     start = mclass(window)
#     window.mainloop()
