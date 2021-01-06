from tkinter import *
from tkinter import ttk

from tkcalendar import DateEntry
from user_data_manager import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from draw_figure import create_subplot, create_currency_chart
from data_manager import *


class CurrencyManager:
    def __init__(self, window: Tk):
        self.window = window

        # Window config
        self.window.title('Menadżer walut')
        self.window.iconphoto(False, PhotoImage(file="resource/icon.png"))
        self.window.geometry('1300x700')
        self.window.minsize(1300, 700)

        # Window right side
        self.window_right = Frame(self.window, borderwidth=2, relief=SOLID)
        self.window_right.pack(side=RIGHT, expand=True, fill="both", padx=5, pady=5)
        self.window_right_top = Frame(self.window_right)
        self.window_right_bottom = PyCurrencyBottomFrame(self.window_right)
        lb_information = Label(self.window_right, text='Informacje', padx=10, font=("Courier", 30, 'bold'))
        lb_currency = Label(self.window_right, text='Kalkulator walutowy', font=("Courier", 30, 'bold'), padx=10)
        lb_information.pack(side=TOP, pady=(10, 10))
        self.window_right_top.pack(side=TOP, fill=X)
        lb_currency.pack(side=TOP)
        self.window_right_bottom.pack(fill=X, pady=(10, 0))

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

        # Instantiate Left Plot
        self.fig = create_subplot()

        # Instantiate Right top side
        self.lb_average_text = Label(self.window_right_top, text='test', font=("Courier", 12), anchor=W)
        self.lb_difference_interval_text = Label(self.window_right_top, text='test', font=("Courier", 12), anchor=W)
        self.lb_difference_one_day_text = Label(self.window_right_top, text='test', font=("Courier", 12), anchor=W)

        self.lb_average_value = Label(self.window_right_top, text='test', font=("Courier", 12, "bold"), anchor=E)
        self.lb_difference_interval_value = Label(self.window_right_top, text='test',
                                                  font=("Courier", 12, "bold"), anchor=E)
        self.lb_difference_one_day_value = Label(self.window_right_top, text='test',
                                                 font=("Courier", 12, "bold"), anchor=E)

        # Adding to top right frame
        self.lb_average_text.grid(row=0, column=0, padx=10, pady=15, sticky=W)
        self.lb_difference_interval_text.grid(row=1, column=0, padx=10, sticky=W)
        self.lb_difference_one_day_text.grid(row=2, column=0, padx=10, pady=15, sticky=W)
        self.lb_average_value.grid(row=0, column=1, padx=10, pady=15, sticky=E)
        self.lb_difference_interval_value.grid(row=1, column=1, padx=10, sticky=E)
        self.lb_difference_one_day_value.grid(row=2, column=1, padx=10, pady=15, sticky=E)
        self.window_right_top.grid_columnconfigure((1,), weight=1)

        # Instantiate Right bottom side
        # self.ent_value = Entry(self.window_right_bottom, font=("Courier", 25, 'bold'), width=4)
        # self.button_convert = Button(self.window_right_bottom, text="Przelicz",
        #                              font=("Courier", 20, 'bold'), command=self.plot)
        # self.button_reverse = Button(self.window_right_bottom, text='Zamień',
        #                              font=("Courier", 20, 'bold'), command=self.plot)
        # self.date_entry = DateEntry(self.window_right_bottom, width=12, borderwidth=2, year=2010)
        # self.lb_currency_result = Label(self.window_right_bottom, font=("Courier", 30, 'bold'), padx=10)
        # self.lb_ent = Label(self.window_right_bottom,
        #                     text='zł',
        #                     font=("Courier", 25, 'bold'))
        # lb_date = Label(self.window_right_bottom, text='Data: ', font=("Courier", 25, 'bold'), padx=10)
        #
        # self.ent_value.grid(row=0, column=1, padx=(10, 0), pady=15, sticky='WENS')
        # self.lb_ent.grid(row=0, column=2, pady=15, sticky='WE')
        # lb_date.grid(row=1, column=1, pady=15, sticky='WE')
        # self.date_entry.grid(row=1, column=2, pady=15, sticky='WENS')
        # self.button_convert.grid(row=2, column=1, pady=15)
        # self.button_reverse.grid(row=2, column=2, pady=15)
        # self.lb_currency_result.grid(row=3, column=1, columnspan=2, pady=15, sticky='WE')
        # self.window_right_bottom.grid_columnconfigure((0, 3), weight=1)

        # Get Config
        self.user_config = UserData.load_from_file()

        # Get Data
        self.data = []

        # Update view with information
        self.update()

    def plot(self):
        create_currency_chart(self.user_config.currency_type, self.data, self.fig)
        canvas = FigureCanvasTkAgg(self.fig, master=self.window_left)
        toolbar = NavigationToolbar2Tk(canvas, self.window_left_bottom)
        toolbar.update()
        canvas.get_tk_widget().pack(padx=(10, 0))
        canvas.draw()

    def update(self):
        self.data = get_currency(self.user_config.currency_type, self.user_config.get_start_date(), get_now_date())
        self.plot()
        self.update_labels()

    def update_labels(self):
        self.lb_average_text.config(text=f'Średnia z {self.user_config.numb_days} dni wynosi: ')
        difference_day = get_difference(self.data[0][1], self.data[len(self.data) - 1][1])
        difference_interval = get_difference(self.data[len(self.data) - 2][1], self.data[len(self.data) - 1][1])
        self.lb_difference_one_day_text.config(text=f'Wartość w ciągu jednego dnia '
                                                    f'{"zmniejszyła" if difference_day < 0 else "zwiekszyła"}'
                                                    f' się o ')
        self.lb_difference_interval_text.config(text=f'Wartość w ciągu {self.user_config.numb_days} '
                                                     f'{"zmniejszyła" if difference_interval < 0 else "zwiekszyła"}'
                                                     f' się o ')
        self.lb_average_value.config(text=f'{get_avg(self.data):10.3f}')
        self.lb_difference_one_day_value.config(text=f'{difference_day:10.3f} %')
        self.lb_difference_interval_value.config(text=f'{difference_interval:10.3f} %')


class PyCurrencyBottomFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.ent_value = Entry(self, font=("Courier", 25, 'bold'), width=4)
        self.button_convert = Button(self, text="Przelicz",
                                     font=("Courier", 20, 'bold'), command=None)
        self.button_reverse = Button(self, text='Zamień',
                                     font=("Courier", 20, 'bold'), command=None)
        self.date_entry = DateEntry(self, width=12, borderwidth=2, year=2010)
        self.lb_currency_result = Label(self, font=("Courier", 30, 'bold'), padx=10)
        self.lb_ent = Label(self,
                            text='zł',
                            font=("Courier", 25, 'bold'))
        lb_date = Label(self, text='Data: ', font=("Courier", 25, 'bold'), padx=10)

        self.ent_value.grid(row=0, column=1, padx=(10, 0), pady=15, sticky='WENS')
        self.lb_ent.grid(row=0, column=2, pady=15, sticky='WE')
        lb_date.grid(row=1, column=1, pady=15, sticky='WE')
        self.date_entry.grid(row=1, column=2, pady=15, sticky='WENS')
        self.button_convert.grid(row=2, column=1, pady=15)
        self.button_reverse.grid(row=2, column=2, pady=15)
        self.lb_currency_result.grid(row=3, column=1, columnspan=2, pady=15, sticky='WE')
        self.grid_columnconfigure((0, 3), weight=1)

    def update_frame(self, user_config):
        self.lb_ent.config(text=f'{"zł" if user_config.is_zl else user_config.currency_type}')
        self.lb_currency_result.config(text=f'0 {"zł" if not user_config.is_zl else user_config.currency_type}')


if __name__ == '__main__':
    root = Tk()
    style = ttk.Style()
    style.theme_use('clam')
    start = CurrencyManager(root)
    # root.protocol("WM_DELETE_WINDOW", func)
    root.mainloop()
