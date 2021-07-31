import ATRI
from ..status import info_msg
from .data_source import Console


driver = ATRI.driver()


async def handle_is_connect():
    data = Console().is_connect()
    return {"status": 200, "is_connect": data}


async def handle_status():
    return {"status": 200, "message": info_msg}


async def handle_dashboard_info():
    data = Console().load_data()
    return {"status": 200, "data": data}
