from ATRI.log import logger as log

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
        except Exception:
            log.error("获取最新推送信息失败...")
            return str()

        try:
            commit_data: dict = data[0]
        except Exception:
            log.error("GitHub 数据结构已更改, 请前往仓库提交 Issue.")
            return str()

        c_info = commit_data["commit"]
        c_msg = c_info["message"]
        c_sha = commit_data["sha"][0:5]
        c_time = c_info["author"]["date"]

        return f"Latest commit {c_msg} | sha: {c_sha} | time: {c_time}"

    @classmethod
    async def show_latest_version(cls) -> tuple:
        try:
            data = await cls._get_release_info()
        except Exception:
            log.error("获取发布列表失败...")
            return str(), str()

        try:
            release_data: dict = data[0]
        except Exception:
            log.error("GitHub 数据结构已更改, 请前往仓库提交 Issue.")
            return str(), str()

        l_v = release_data["tag_name"]
        l_v_t = release_data["published_at"]
        return l_v, l_v_t
