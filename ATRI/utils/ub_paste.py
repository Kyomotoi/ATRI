from aiohttp import ClientSession


URL = "https://paste.ubuntu.com/"


async def paste(form_data) -> str:
    async with ClientSession() as session:
        async with session.post(url=URL, data=form_data) as r:
            result = str(r.url).replace("https://", "")
            return result
