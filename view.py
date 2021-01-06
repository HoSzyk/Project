from tkinter import *
from tkinter import ttk

from tkcalendar import DateEntry
from user_data_manager import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from draw_figure import create_subplot, create_currency_chart
from data_manager import *


class CurrencyManager(Frame):
    def __init__(self, window, *args, **kwargs):
        Frame.__init__(self, window, *args, **kwargs)
        self.window = window

        # Window config
        self.window.title('Menadżer walut')
        self.window.iconphoto(False, PhotoImage(file="resource/icon.png"))
        self.window.geometry('1300x700')
        self.window.minsize(1300, 700)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Window right side
        self.window_right = Frame(self.window, borderwidth=2, relief=SOLID)
        self.window_right.pack(side=RIGHT, expand=True, fill="both", padx=5, pady=5)
        self.window_right_top = PyCurrencyTopFrame(self.window_right)
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
        main_menu.add_command(label="Odśwież bazę danych", command=self.update_db)
        main_menu.add_command(label="Ustawienia", command=self.call_options)
        self.window.config(menu=main_menu)

        # Instantiate Left Plot
        self.fig = create_subplot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window_left)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window_left_bottom)
        self.canvas.get_tk_widget().pack(padx=(10, 0))

        # Get Config
        self.user_config = UserData.load_from_file()

        # Get Data
        self.data = []

        # Update view with information
        self.update()

    def update_plot(self):
        create_currency_chart(self.user_config.currency_type, self.data, self.fig)
        self.toolbar.update()
        self.canvas.draw()

    def update_db(self):
        fill_currency(self.user_config.currency_type, self.user_config.get_start_date(), get_now_date())
        self.update()

    def on_close(self):
        self.user_config.save_to_file()
        self.window.destroy()

    def call_options(self):
        options_popup = Options(self)
        options_popup.wait_window()

    def update(self):
        self.data = get_currency(self.user_config.currency_type, self.user_config.get_start_date(), get_now_date())
        self.update_plot()
        self.window_right_top.update_frame(self.user_config, self.data)
        self.window_right_bottom.update_frame(self.user_config)


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


class PyCurrencyTopFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Instantiate Right top side
        self.lb_average_text = Label(self, text='test', font=("Courier", 12), anchor=W)
        self.lb_difference_interval_text = Label(self, text='test', font=("Courier", 12), anchor=W)
        self.lb_difference_one_day_text = Label(self, text='test', font=("Courier", 12), anchor=W)

        self.lb_average_value = Label(self, text='test', font=("Courier", 12, "bold"), anchor=E)
        self.lb_difference_interval_value = Label(self, text='test',
                                                  font=("Courier", 12, "bold"), anchor=E)
        self.lb_difference_one_day_value = Label(self, text='test',
                                                 font=("Courier", 12, "bold"), anchor=E)
        self.lb_average_text.grid(row=0, column=0, padx=10, pady=15, sticky=W)
        self.lb_difference_interval_text.grid(row=1, column=0, padx=10, sticky=W)
        self.lb_difference_one_day_text.grid(row=2, column=0, padx=10, pady=15, sticky=W)
        self.lb_average_value.grid(row=0, column=1, padx=10, pady=15, sticky=E)
        self.lb_difference_interval_value.grid(row=1, column=1, padx=10, sticky=E)
        self.lb_difference_one_day_value.grid(row=2, column=1, padx=10, pady=15, sticky=E)
        self.grid_columnconfigure((1,), weight=1)

    def update_frame(self, user_config, data):
        self.lb_average_text.config(text=f'Średnia z {user_config.numb_days} dni wynosi: ')
        difference_day = get_difference(data[0][1], data[len(data) - 1][1])
        difference_interval = get_difference(data[len(data) - 2][1], data[len(data) - 1][1])
        self.lb_difference_one_day_text.config(text=f'Wartość w ciągu jednego dnia '
                                                    f'{"zmniejszyła" if difference_day < 0 else "zwiekszyła"}'
                                                    f' się o ')
        self.lb_difference_interval_text.config(text=f'Wartość w ciągu {user_config.numb_days} '
                                                     f'{"zmniejszyła" if difference_interval < 0 else "zwiekszyła"}'
                                                     f' się o ')
        self.lb_average_value.config(text=f'{get_avg(data):10.3f}')
        self.lb_difference_one_day_value.config(text=f'{difference_day:10.3f} %')
        self.lb_difference_interval_value.config(text=f'{difference_interval:10.3f} %')


class Options(Toplevel):
    def __init__(self, parent: CurrencyManager):
        Toplevel.__init__(self, parent)
        self.parent = parent

        # add an entry widget
        self.e1 = Entry(self)
        self.e1.pack()

        # add a button
        b1 = Button(self, text="Popup button", command=self.button_pressed)
        b1.pack()

    def button_pressed(self):
        # self.parent.user_config = self.e1.get()
        self.exit_popup()

    def exit_popup(self):
        self.destroy()


if __name__ == '__main__':
    root = Tk()
    style = ttk.Style()
    style.theme_use('clam')
    start = CurrencyManager(root)
    root.mainloop()
