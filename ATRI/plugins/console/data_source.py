import os
import json
from pathlib import Path
from datetime import datetime

from ATRI.service import Service


CONSOLE_DIR = Path(".") / "data" / "database" / "console"
os.makedirs(CONSOLE_DIR, exist_ok=True)


is_connect = False


class Console(Service):
    def __init__(self):
        Service.__init__(self, "控制台")

    @staticmethod
    def record_data(data: dict) -> None:
        now_time = datetime.now().strftime("%Y-%m-%d")
        file_name = f"{now_time}-runtime.json"
        path = CONSOLE_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps(list()))
            temp_data = list()

        temp_data: list = json.loads(path.read_bytes())
        temp_data.append(data)
        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(temp_data, indent=4))

    @staticmethod
    def load_data() -> list:
        now_time = datetime.now().strftime("%Y-%m-%d")
        file_name = f"{now_time}-runtime.json"
        path = CONSOLE_DIR / file_name
        if not path.is_file():
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps(list()))
            return list()

        data: list = json.loads(path.read_bytes())
        return data

    @staticmethod
    def store_connect_stat(i: bool):
        global is_connect
        is_connect = i

    @staticmethod
    def is_connect() -> bool:
        return is_connect
