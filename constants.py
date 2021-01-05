from enum import Enum
from datetime import datetime


class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    CHF = 'CHF'


REQUEST_LIMIT = 366
FIRST_DAY = datetime.strptime('2002-01-02', '%Y-%m-%d')
LAST_DAY = datetime.strptime('2020-12-17', '%Y-%m-%d')
CONFIG_FILE_PATH = 'config.json'
