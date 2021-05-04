from ATRI.utils.request import post_bytes


URL = "https://saucenao.com/search.php"


class SauceNao:
    def __init__(
        self, api_key: str, output_type=2, testmode=1, dbmaski=32768, db=5, numres=5
    ) -> None:
        params = dict()
        params["api_key"] = api_key
        params["output_type"] = output_type
        params["testmode"] = testmode
        params["dbmaski"] = dbmaski
        params["db"] = db
        params["numres"] = numres
        self.params = params

    async def search(self, url: str):
        self.params["url"] = url
        res = await post_bytes(url=URL, params=self.params)
        return res
