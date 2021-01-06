from tkinter import *
from tkcalendar import DateEntry
from user_data_manager import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from draw_figure import create_subplot, create_currency_chart
from data_manager import get_currency


class CurrencyManager:
    def __init__(self, window: Tk):
        self.window = window

        # Window config
        self.window.title('Menadżer walut')
        self.window.iconphoto(False, PhotoImage(file="resource/icon.png"))

        # Window right side
        self.window_right = Frame(self.window)
        self.window_right.pack(side=RIGHT, expand=True, fill="both")
        self.window_right_bottom = Frame(self.window_right)
        self.window_right_bottom.pack(side=BOTTOM, expand=True, fill="both")

        # Window left side
        self.window_left = Frame(self.window)
        self.window_left.pack(side=LEFT, expand=True, fill="both", padx=(0, 20))
        self.window_left_bottom = Frame(self.window_left)
        self.window_left_bottom.pack(side=BOTTOM, expand=True, fill="both", padx=(0, 60))

        # Instantiate Menu
        main_menu = Menu(self.window)
        main_menu.add_command(label="Odśwież bazę danych", command=None)
        main_menu.add_command(label="Ustawienia", command=None)
        self.window.config(menu=main_menu)

        # Instantiate Plot
        self.fig = create_subplot()
        self.plot()

        # Instantiate Right side
        self.lb_average = Label(self.window_right, text='test')
        self.lb_difference_interval = Label(self.window_right, text='test')
        self.lb_difference_one_day = Label(self.window_right, text='test')
        self.lb_average.pack(padx=10, pady=10, expand=True, fill="both")
        self.lb_difference_interval.pack(padx=10, pady=10, expand=True, fill="both")
        self.lb_difference_one_day.pack(padx=10, pady=10, expand=True, fill="both")

        # Instantiate Right bottom side
        self.box = Entry(self.window_right_bottom)
        self.button = Button(self.window_right_bottom, text="check", command=self.plot)
        self.date_entry = DateEntry(self.window_right_bottom, width=12, borderwidth=2, year=2010)
        self.button.pack(side=RIGHT)
        self.date_entry.pack(side=RIGHT)
        self.box.pack(side=LEFT)

        # Get Config
        user_config = UserData.load_from_file()

    def plot(self):
        currency = 'USD'
        data = get_currency(currency, '2020-10-10', '2021-01-05')
        create_currency_chart(currency, data, self.fig)
        canvas = FigureCanvasTkAgg(self.fig, master=self.window_left)
        toolbar = NavigationToolbar2Tk(canvas, self.window_left_bottom)
        toolbar.update()
        canvas.get_tk_widget().pack(padx=(10, 0))
        canvas.draw()


if __name__ == '__main__':
    root = Tk()
    start = CurrencyManager(root)
    # root.protocol("WM_DELETE_WINDOW", func)
    root.mainloop()
