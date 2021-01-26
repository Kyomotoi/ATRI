import os
from pathlib import Path


SERVICE_PATH = Path('.') / 'ATRI' / 'data' / 'service'
ERROR_PATH = Path('.') / 'ATRI' / 'data' / 'error'
os.makedirs(SERVICE_PATH, exist_ok=True)
os.makedirs(ERROR_PATH, exist_ok=True)

state = 0
