from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkcalendar import DateEntry

from data_manager import *
from draw_figure import create_subplot, create_currency_chart_clear_previous
from user_data_manager import *


class CurrencyManager(Frame):
    def __init__(self, window, *args, **kwargs):
        Frame.__init__(self, window, *args, **kwargs)
        self.pack()
        self.window = window

        # Window config
        self.window.title('Menadżer walut')
        self.window.iconphoto(False, PhotoImage(file="resource/icon.png"))
        self.window.geometry('1300x700')
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Window right side
        self.window_right = Frame(self, borderwidth=2, relief=SOLID)
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
        self.window_left = Frame(self)
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
        create_currency_chart_clear_previous(self.user_config.currency_type, self.data, self.fig)
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
        options_popup.grab_set()
        options_popup.wait_window()
        options_popup.grab_release()
        self.update_db()

    def update(self):
        self.data = get_currency(self.user_config.currency_type, self.user_config.get_start_date(), get_now_date())
        self.update_plot()
        self.window_right_top.update_frame(self.user_config, self.data)
        self.window_right_bottom.update_frame(self.user_config)


class PyCurrencyBottomFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Make variables
        self.var_ent = StringVar(self)
        self.var_ent.set('0')

        # Instantiate widgets
        ent_value = Entry(self, textvariable=self.var_ent, font=("Courier", 25, 'bold'), width=4, justify='right')
        self.button_convert = Button(self, text="Przelicz",
                                     font=("Courier", 20, 'bold'), command=self.convert_currency)
        self.button_reverse = Button(self, text='Zamień',
                                     font=("Courier", 20, 'bold'), command=self.reverse_currency_type)
        self.date_entry = DateEntry(self, width=12, borderwidth=2, justify='center', date_pattern='dd-mm-yyyy',
                                    showothermonthdays=False, locale='pl_PL')
        self.lb_currency_result = Label(self, font=("Courier", 30, 'bold'), padx=10)
        self.lb_ent = Label(self,
                            text='PLN',
                            font=("Courier", 25, 'bold'))
        lb_date = Label(self, text='Data: ', font=("Courier", 25, 'bold'), padx=10)

        ent_value.grid(row=0, column=1, padx=(10, 0), pady=15, sticky='WENS')
        self.lb_ent.grid(row=0, column=2, pady=15, sticky='WE')
        lb_date.grid(row=1, column=1, pady=15, sticky='WE')
        self.date_entry.grid(row=1, column=2, pady=15, sticky='WENS')
        self.button_convert.grid(row=2, column=1, pady=15)
        self.button_reverse.grid(row=2, column=2, pady=15)
        self.lb_currency_result.grid(row=3, column=1, columnspan=2, pady=15, sticky='WE')
        self.grid_columnconfigure((0, 3), weight=1)

        # Variables
        self.user_config = None

    def update_frame(self, user_config):
        self.user_config = user_config

        self.lb_ent.config(text=f'{"PLN" if self.user_config.is_zl else self.user_config.currency_type}')
        self.lb_currency_result.config(
            text=f'0 {"PLN" if not self.user_config.is_zl else self.user_config.currency_type}')
        self.date_entry.set_date(get_now_date())

    def reverse_currency_type(self):
        entry_val = self.var_ent.get()
        self.user_config.is_zl = not self.user_config.is_zl
        self.lb_ent.config(text=f'{"PLN" if self.user_config.is_zl else self.user_config.currency_type}')
        currency_result = self.lb_currency_result.cget('text')[:-4]
        self.var_ent.set(currency_result)
        self.lb_currency_result.config(
            text=f'{f"{entry_val} PLN" if not self.user_config.is_zl else f"{entry_val} {self.user_config.currency_type}"}')

    def convert_currency(self):
        currency = 'PLN' if not self.user_config.is_zl else self.user_config.currency_type
        entry = float(self.var_ent.get())
        conv_ent = self.date_entry.get_date()
        conv_date = datetime.combine(conv_ent, time.min)
        currency_record = get_currency(self.user_config.currency_type, conv_date, conv_date)
        if currency_record:
            currency_value = currency_record[0][1]
            result = entry / currency_value if currency != 'PLN' else entry * currency_value
            self.lb_currency_result.config(text=f'{result:5.3f} {currency}')


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
        difference_interval = get_difference(data[0][1], data[-1][1])
        difference_day = get_difference(data[-2][1], data[-1][1])
        self.lb_difference_one_day_text.config(text=f'Wartość w ciągu jednego dnia '
                                                    f'{"zmniejszyła" if difference_day < 0 else "zwiekszyła"}'
                                                    f' się o ')
        self.lb_difference_interval_text.config(text=f'Wartość w ciągu {user_config.numb_days} '
                                                     f'{"zmniejszyła" if difference_interval < 0 else "zwiekszyła"}'
                                                     f' się o ')
        self.lb_average_value.config(text=f'{get_avg(data):10.3f} ')
        self.lb_difference_one_day_value.config(text=f'{difference_day:10.3f}%')
        self.lb_difference_interval_value.config(text=f'{difference_interval:10.3f}%')


class Options(Toplevel):
    def __init__(self, parent: CurrencyManager):
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.title('Ustawienia')
        self.iconphoto(False, PhotoImage(file="resource/settings_icon.png"))

        # Make variables
        currency_types = [e.value for e in const.Currency]
        self.var_currency_type = StringVar(self)
        self.var_currency_type.set(self.parent.user_config.currency_type)

        self.var_days = IntVar(self)
        self.var_days.set(self.parent.user_config.numb_days)

        # Instantiate widgets
        lb_curr = Label(self, text='Waluta ', font=("Courier", 12), anchor=W)
        lb_days = Label(self, text='Ilość dni ', font=("Courier", 12), anchor=W)
        option_currency_type = OptionMenu(self, self.var_currency_type, *currency_types)
        en_days = Entry(self, textvariable=self.var_days)
        but_confirm = Button(self, text="Zatwierdź", command=self.button_pressed)
        but_cancel = Button(self, text="Anuluj", command=self.exit_popup)

        lb_curr.grid(row=0, column=0, padx=10, pady=15, sticky=W)
        option_currency_type.grid(row=0, column=1, padx=10, pady=15, sticky=W)
        lb_days.grid(row=1, column=0, padx=10, pady=15, sticky=W)
        en_days.grid(row=1, column=1, padx=10, pady=15, sticky=W)
        but_confirm.grid(row=2, column=0, padx=30, pady=15, sticky=W)
        but_cancel.grid(row=2, column=1, padx=(0, 30), pady=15, sticky=E)

    def button_pressed(self):
        self.parent.user_config.currency_type = self.var_currency_type.get()
        self.parent.user_config.numb_days = self.var_days.get()
        self.exit_popup()

    def exit_popup(self):
        self.destroy()


def start():
    root = Tk()
    style = ttk.Style()
    style.theme_use('clam')
    CurrencyManager(root)
    root.mainloop()


if __name__ == '__main__':
    start()
