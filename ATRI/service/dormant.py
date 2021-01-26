from ATRI.exceptions import InvalidSetting

from . import state

class Dormant:
    @staticmethod
    def is_sleep() -> bool:
        return True if state != 1 else False

    @staticmethod
    def cont_wake(_type: bool) -> None:
        global state
        try:
            if _type:
                state = 0
            else:
                state = 1
        except InvalidSetting:
            raise InvalidSetting('Failed to modify variable!')
