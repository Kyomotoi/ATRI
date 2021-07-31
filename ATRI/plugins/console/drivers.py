from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import ATRI
from .view import handle_is_connect, handle_dashboard_info, handle_status


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:20000",
]


def register_route():
    app = ATRI.driver().server_app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    static_path = str(
        (Path(".") / "ATRI" / "plugins" / "console" / "atri-manege" / "dist").absolute()
    )

    app.get("/bot/is_connect")(handle_is_connect)
    app.get("/bot/status")(handle_status)
    app.get("/bot/dashboard_info")(handle_dashboard_info)

    app.mount("/", StaticFiles(directory=static_path, html=True), name="bot")
