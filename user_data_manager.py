import json
from constants import *


class UserData:
    def __init__(self):
        self.currency_type = ''
        self.numb_days = 0

    @classmethod
    def load_from_file(cls, file_path=CONFIG_FILE_PATH):
        user_data = UserData()
        with open(file_path, 'r') as read_file:
            data = json.load(read_file)
        user_data.currency_type = data['currency_type']
        user_data.numb_days = data['numb_days']
        return user_data

    def save_to_file(self, file_path=CONFIG_FILE_PATH):
        with open(file_path, 'w+') as write_file:
            data = {
                'currency_type': self.currency_type,
                'numb_days': self.numb_days
            }
            json.dump(data, write_file, indent=4)
