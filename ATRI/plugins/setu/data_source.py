from pathlib import Path

from ATRI.config import SETU_CONFIG

DATA_PATH = Path('.') / 'ATRI' / 'data' / 'database'

class Function:
    @staticmethod
    async def setu_port() -> str:
        ...
    
    @staticmethod
    async def setu_local() -> str:
        ...
