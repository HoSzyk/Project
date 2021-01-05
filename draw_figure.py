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
                sub_plot.plot(*zip(*response), label=currency)
                max_x, max_y = max(response, key=lambda x: x[1])
                sub_plot.annotate('Maksimum', xy=(max_x, max_y), xytext=(max_x, max_y + 0.03),
                                  arrowprops=dict(arrowstyle='->'), clip_on=True,
                                  )
                sub_plot.tick_params(axis='x', rotation=45)
    sub_plot.legend()
    return fig


def create_subplot(fig=Figure(figsize=(8, 8))):
    fig.subplots_adjust(left=0.1, right=0.9, top=1, bottom=0.12)
    fig.patch.set_color('#F0F0F0')
    sub_plot = fig.add_subplot(111)
    sub_plot.set_xlabel('Data', fontsize=15, fontweight='bold')
    sub_plot.set_ylabel('Wartosc waluty [PLN]', fontsize=15, fontweight='bold')

    return fig
