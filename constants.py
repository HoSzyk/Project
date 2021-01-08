from enum import Enum
from pathlib import Path


class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'
    CHF = 'CHF'


REQUEST_LIMIT = 366
CONFIG_FILE_PATH = Path(__file__).parent / "./Data/config.json"
DATABASE_PATH = Path(__file__).parent / "./Data/database.db"
