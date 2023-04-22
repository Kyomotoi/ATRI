from ATRI.utils import request
from ATRI.exceptions import RequestError


class API:
    def __init__(self, uid: int):
        self.uid = uid

    async def _request(self, url: str, params: dict = dict()) -> dict:
        headers = {
            "User-Agent": "Mozilla/5.0",
        }

        try:
            resp = await request.get(url, params=params, headers=headers)
        except Exception:
            raise RequestError("Request failed!")

        return resp.json()

    async def get_user_info(self) -> dict:
        url = "https://api.bilibili.com/x/space/acc/info"
        params = {"mid": self.uid}
        return await self._request(url, params)

    async def get_user_dynamics(
        self, offset: int = int(), need_top: bool = False
    ) -> dict:
        url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"
        params = {
            "host_uid": self.uid,
            "offset_dynamic_id": offset,
            "need_top": 1 if need_top else 0,
        }
        return await self._request(url, params)
