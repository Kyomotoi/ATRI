import json
from typing import List

from ATRI.utils import request
from ATRI.message import MessageBuilder

from .models import SauceNAORequest, SauceNAOResponse, SauceNAOResult

SAUCENAO_URL: str = "https://saucenao.com/search.php"


class SauceNAO:
    def __init__(
        self,
        api_key: str,
        output_type: int = 2,
        testmode: int = 1,
        dbmaski: int = 32768,
        db: int = 5,
        numres: int = 5,
    ) -> None:
        self.params = SauceNAORequest(
            api_key=api_key,
            output_type=output_type,
            testmode=testmode,
            dbmaski=dbmaski,
            db=db,
            numres=numres,
        )

    async def _request(self, url: str) -> SauceNAOResponse:
        self.params.url = url
        resp = await request.get(SAUCENAO_URL, params=self.params.dict())
        return SauceNAOResponse.parse_obj(resp.json())

    async def search(self, url: str) -> str:
        try:
            data = await self._request(url)
        except Exception as err:
            raise Exception(f"处理 SauceNAO 数据失败：{str(err)}")

        r: List[SauceNAOResult] = list()
        for i in range(3):
            _data = data.results[i]
            sim = _data.header.similarity
            if float(sim) >= 70:
                r.append(
                    SauceNAOResult(
                        similarity=sim,
                        index_name=_data.header.index_name,
                        url=_data.data.ext_urls[0] if _data.data.ext_urls else "None",
                    )
                )

        if not r:
            return "SauceNAO 中没有相似的结果"

        result = str()
        for i in r:
            result += (
                MessageBuilder("\n——————————")
                .text(f"相似度：{i.similarity}")
                .text(f"名称：{i.index_name}")
                .text(f"URL: {i.url.replace('https://', str()).replace('http://', str())}")
                .done()
            )
        return result
