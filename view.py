from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from draw_figure import create_subplot, create_currency_chart
from main import get_currency, fill_currency


class CurrencyManager:
    def __init__(self, window):
        self.window = window
        self.box = Entry(window)
        self.button = Button(window, text="check", command=self.plot)
        self.box.pack()
        self.button.pack()
        self.fig = create_subplot()

    def plot(self):
        currency = 'USD'
        data = get_currency(currency, '2020-10-10', '2021-01-05')
        create_currency_chart(currency, data, self.fig)
        canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        toolbar = NavigationToolbar2Tk(canvas, self.window)
        toolbar.update()
        canvas.get_tk_widget().pack()
        canvas.draw()


if __name__ == '__main__':
    win = Tk()
    start = CurrencyManager(win)
    win.mainloop()
