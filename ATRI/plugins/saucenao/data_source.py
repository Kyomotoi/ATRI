from random import choice

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.exceptions import RequestError
from ATRI.utils import request


URL = "https://saucenao.com/search.php"


class SaouceNao(Service):
    def __init__(
        self,
        api_key: str = str(),
        output_type=2,
        testmode=1,
        dbmaski=32768,
        db=5,
        numres=5,
    ):
        Service.__init__(self, "以图搜图", "以图搜图，仅限二刺螈", rule=is_in_service("以图搜图"))

        params = dict()
        params["api_key"] = api_key
        params["output_type"] = output_type
        params["testmode"] = testmode
        params["dbmaski"] = dbmaski
        params["db"] = db
        params["numres"] = numres
        self.params = params

    async def _request(self, url: str):
        self.params["url"] = url
        try:
            res = await request.get(URL, params=self.params)
        except RequestError:
            raise RequestError("Request failed!")
        data = res.json()
        return data

    async def search(self, url: str) -> str:
        data = await self._request(url)
        try:
            res = data.get("results", "result")
        except:
            return "没有相似的结果呢..."

        r = list()
        for i in range(3):
            data = res[i]

            sim = data["header"]["similarity"]
            if float(sim) >= 70:
                _result = dict()
                _result["similarity"] = sim
                _result["index_name"] = data["header"]["index_name"]
                _result["url"] = choice(data["data"].get("ext_urls", ["None"]))
                r.append(_result)

        if not r:
            return "没有相似的结果呢..."

        msg0 = str()
        for i in r:
            msg0 += (
                "\n——————————\n"
                f"Similarity: {i['similarity']}\n"
                f"Name: {i['index_name']}\n"
                f"URL: {i['url'].replace('https://', '')}"
            )

        return msg0
