from datetime import timedelta

from matplotlib.figure import Figure


def create_currency_chart(currency, data, fig):
    sub_plot = fig.get_axes()[0]
    if not data:
        print('No data')
    else:
        sub_plot.plot(*zip(*data), label=currency)
        max_x, max_y = max(data, key=lambda x: x[1])
        min_x, min_y = min(data, key=lambda x: x[1])
        sub_plot.annotate('Maksimum', xy=(max_x, max_y), xytext=(max_x, max_y + 0.03),
                          arrowprops=dict(arrowstyle='->'), clip_on=True,
                          )
        sub_plot.tick_params(axis='x', rotation=45)
        sub_plot.set_ylim([min_y - 0.01 * min_y, max_y + 0.02 * max_y])
        sub_plot.set_xlim([data[0][0], data[len(data) - 1][0] + timedelta(days=2)])
    sub_plot.legend()
    return fig


def create_subplot(fig=Figure(figsize=(8, 8))):
    fig.subplots_adjust(left=0.1, right=0.9, top=1, bottom=0.12)
    fig.patch.set_color('#F0F0F0')
    sub_plot = fig.add_subplot(111)
    sub_plot.set_xlabel('Data', fontsize=10, fontweight='bold')
    sub_plot.set_ylabel('Wartosc waluty [PLN]', fontsize=10, fontweight='bold')
    return fig
