from ATRI.exceptions import RequestError

from . import request


REPO_COMMITS_URL = "https://api.github.com/repos/Kyomotoi/ATRI/commits"
REPO_RELEASE_URL = "https://api.github.com/repos/Kyomotoi/ATRI/releases"


class CheckUpdate:
    @staticmethod
    async def _get_commits_info() -> dict:
        req = await request.get(REPO_COMMITS_URL)
        return req.json()

    @staticmethod
    async def _get_release_info() -> dict:
        req = await request.get(REPO_RELEASE_URL)
        return req.json()

    @classmethod
    async def show_latest_commit_info(cls) -> str:
        try:
            data = await cls._get_commits_info()
        except RequestError:
            raise RequestError("Getting commit info timeout...")

        try:
            commit_data: dict = data[0]
        except Exception:
            raise Exception("GitHub has been error!!!")

        c_info = commit_data["commit"]
        c_msg = c_info["message"]
        c_sha = commit_data["sha"][0:5]
        c_time = c_info["author"]["date"]

        return f"Latest commit {c_msg} | sha: {c_sha} | time: {c_time}"

    @classmethod
    async def show_latest_version(cls) -> tuple:
        try:
            data = await cls._get_release_info()
        except RequestError:
            raise RequestError("Getting release list timeout...")

        try:
            release_data: dict = data[0]
        except Exception:
            raise Exception("GitHub has been error!!!")

        l_v = release_data["tag_name"]
        l_v_t = release_data["published_at"]
        return l_v, l_v_t
