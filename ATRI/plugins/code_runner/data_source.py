from ATRI.utils import request
from ATRI.message import MessageBuilder
from ATRI.exceptions import RequestError


RUN_API_URL_FORMAT = "https://glot.io/run/{}?version=latest"
SUPPORTED_LANGUAGES = {
    "assembly": {"ext": "asm"},
    "bash": {"ext": "sh"},
    "c": {"ext": "c"},
    "clojure": {"ext": "clj"},
    "coffeescript": {"ext": "coffe"},
    "cpp": {"ext": "cpp"},
    "csharp": {"ext": "cs"},
    "erlang": {"ext": "erl"},
    "fsharp": {"ext": "fs"},
    "go": {"ext": "go"},
    "groovy": {"ext": "groovy"},
    "haskell": {"ext": "hs"},
    "java": {"ext": "java", "name": "Main"},
    "javascript": {"ext": "js"},
    "julia": {"ext": "jl"},
    "kotlin": {"ext": "kt"},
    "lua": {"ext": "lua"},
    "perl": {"ext": "pl"},
    "php": {"ext": "php"},
    "python": {"ext": "py"},
    "ruby": {"ext": "rb"},
    "rust": {"ext": "rs"},
    "scala": {"ext": "scala"},
    "swift": {"ext": "swift"},
    "typescript": {"ext": "ts"},
}


class CodeRunner:
    @staticmethod
    def help() -> str:
        return (
            MessageBuilder("/code {语言}")
            .text("{代码}")
            .text("For example:")
            .text("/code python")
            .text("print('hello world')")
            .done()
        )

    @staticmethod
    def list_supp_lang() -> str:
        msg0 = "咱现在支持的语言如下：\n"
        msg0 += ", ".join(map(str, SUPPORTED_LANGUAGES.keys()))
        return msg0

    @staticmethod
    async def runner(msg: str):
        args = msg.split("\n")
        if not args:
            return "请检查键入内容..."

        try:
            _ = args[1]
        except Exception:
            return "请检查键入内容...需要帮助：/code help"

        lang = args[0].replace("\r", "")
        if lang not in SUPPORTED_LANGUAGES:
            return "该语言暂不支持...或者可能格式错误？"

        del args[0]
        code = "\n".join(map(str, args))
        url = RUN_API_URL_FORMAT.format(lang)
        js = {
            "files": [
                {
                    "name": (
                        SUPPORTED_LANGUAGES[lang].get("name", "main")
                        + f".{SUPPORTED_LANGUAGES[lang]['ext']}"
                    ),
                    "content": code,
                }
            ],
            "stdin": "",
            "command": "",
        }

        try:
            res = await request.post(url, json=js)
        except Exception:
            raise RequestError("Request failed!")

        payload = res.json()
        sent = False
        for k in ["stdout", "stderr", "error"]:
            v = payload.get(k)
            lines = v.splitlines()
            lines, remained_lines = lines[:10], lines[10:]
            out = "\n".join(lines)
            out, remained_out = out[: 60 * 10], out[60 * 10 :]

            if remained_lines or remained_out:
                out += f"\n（太多了太多了...）"

            if out:
                return f"\n{k}:\n{out}"

        if not sent:
            return "\n运行完成，没任何输出呢..."
