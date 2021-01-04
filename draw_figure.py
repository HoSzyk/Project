from matplotlib.figure import Figure
from main import get_previous_days


def create_currency_chart(currencies, days, fig):
    sub_plot = fig.get_axes()[0]
    if not isinstance(currencies, list) or days < 1:
        print('Invalid arguments, please try again')
    else:
        for currency in currencies:
            response = get_previous_days(currency, days)
            if isinstance(response, int) or response is None:
                print(f'Failed fetching {currency}')
            else:
                sub_plot.plot(*zip(*response))

    return fig


def create_subplot(fig=Figure(figsize=(8, 8))):
    sub_plot = fig.add_subplot(111)
    sub_plot.set_xlabel('Data')
    sub_plot.set_ylabel('Wartosc waluty [PLN]')
    return fig
