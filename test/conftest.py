import pytest

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

from nonebug import NONEBOT_INIT_KWARGS


def pytest_configure(config: pytest.Config):
    config.stash[NONEBOT_INIT_KWARGS] = {
        "superusers": {"1145141919"},
        "command_start": {""},
    }


@pytest.fixture(scope="session", autouse=True)
def load_bot(nonebug_init: None):
    driver = nonebot.get_driver()
    driver.register_adapter(OnebotV11Adapter)

    nonebot.load_plugins("ATRI/plugins")
