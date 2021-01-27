import os
from pathlib import Path


TEMP_PATH = Path('.') / 'ATRI' / 'data' / 'temp' / 'img'
os.makedirs(TEMP_PATH, exist_ok=True)
