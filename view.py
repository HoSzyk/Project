from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from draw_figure import create_subplot, create_currency_chart
from data_manager import get_currency


class CurrencyManager:
    def __init__(self, window:Tk):
        self.window = window

        # Window config
        self.window.title('Menadżer walut')
        self.window.iconphoto(False, PhotoImage(file="resource/icon.png"))

        self.box = Entry(window)
        self.button = Button(window, text="check", command=self.plot)
        self.box.pack()
        self.button.pack()

        # Instantiate Menu
        main_menu = Menu(self.window)
        main_menu.add_command(label="Odśwież", command=None)
        main_menu.add_command(label="Ustawienia", command=None)
        self.window.config(menu=main_menu)

        # Instantiate Plot
        self.fig = create_subplot()
        self.plot()

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
    root = Tk()
    start = CurrencyManager(root)
    # root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
