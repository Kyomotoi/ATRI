from pathlib import Path
from ipaddress import IPv4Address

from .data_source import Console, C


console = Console(C())


def init_config(conf_path: Path, default_conf_path: Path):
    console.print("\n[b]アトリは、高性能ですから！[/b]\n", style="#00bee6")

    console.warn("文档地址: https://atri.imki.moe")
    console.info("这是你第一次启动本项目, 请根据提示填写信息")
    console.info("如中途填写错, 你可以直接退出, 再次启动以重新填写")
    console.info("如需使用默认值, Enter 跳过方可\n")

    console.info("[b]Bot 主体设置[/b]\n", style="white")
    host = console.input(
        "Bot 监听的主机名 (IP). 如有控制台相关需求, 建议: [green]0.0.0.0[/green] (默认: [green]127.0.0.1[/green])",
        "127.0.0.1",
        IPv4Address,
        "输入不正确 示例: 127.0.0.1",
    )
    port = console.input(
        "Bot 对外开放的端口 (Port). 范围建议: [green]10000-60000[/green] (默认: [green]20000[/green])",
        "20000",
        int,
        "输入不正确 示例: 20000",
    )
    superusers = console.input(
        "超级用户 (qq号), 即 Bot 的[b]主人[/b]. 可填多个, 用英文逗号 (,) 隔开 (默认: [green]1145141919[/green])",
        "1145141919810",
        str,
        "输入不正确 示例: 1145141919",
    )
    access_token = console.input(
        "协议端通信密钥, 此项留空[b]将无法进入控制台[/b]. 无长度限制 示例: [green]21^sASDA!@3l67GJlk7sd!14#[/green]",
        str(),
        str,
        "输入不正确 示例: 21^sASDA!@3l67GJlk7sd!14# (请尽可能复杂, 无长度限制)",
    )
    proxy = console.input(
        "是否有代理. 格式参考: http(s)://127.0.0.1:8100 (如无请 Enter 以跳过)",
        str(),
        str,
        "输入不正确 示例: http://127.0.0.1:8100",
    )
    console.success("Bot 主体配置完成\n")

    console.info("[b]Bot 进阶设置[/b]\n", style="white")
    is_use_with_gocq = console.input(
        "是否启用内置的 gocqhttp? (y/n) (默认: y)", "y", str, "输入不正确 示例: y"
    )
    if is_use_with_gocq in ["y", "Y", "true", "True", "是"]:
        uin = console.input("Bot 账号", "1145141919", int, "输入不正确 示例: 1145141919")
        password = console.input(
            "Bot 账号密码 (已做隐藏处理, 如不确定是否填写正确, 请查阅填写完毕后所生成的文件: config.yml)",
            str(),
            str,
            password=True,
        )
        protocol = console.input(
            "Bot 登录设备类型. 范围: 0-5, 具体请参考文档: 部署项目-设置 (默认: 5)",
            "5",
            int,
            "输入不正确 范围 0-5 示例: 5",
        )
        download_domain = console.input(
            "gocqhttp 下载源域名设置. 具体请参考文档: 部署项目-设置 (默认: github.com)", "github.com"
        )
        is_use_with_gocq = True
        console.success("内置 gocqhttp 配置完成. 支持多账号, 具体请参考文档: 部署项目-设置\n")
    else:
        is_use_with_gocq = False
        console.info("已跳过\n")

    console.info("[b]Bot 插件设置[/b]\n", style="white")
    saucenao_key = console.input(
        "SauceNAO 搜图密钥, 如不填写将无法启用[b]以图搜图[/b], 前往官网以获取: https://saucenao.com/ (默认: 空)",
        str(),
        str,
    )

    console.success("[white]至此, 所需基本配置已填写完毕[white]")

    raw_conf = default_conf_path.read_text("utf-8")
    raw_conf = raw_conf.replace("{host}", str(host))
    raw_conf = raw_conf.replace("{port}", str(port))
    raw_conf = raw_conf.replace("{superusers}", str(superusers.split(",")))
    raw_conf = raw_conf.replace("{access_token}", access_token)
    raw_conf = raw_conf.replace("{proxy}", proxy)

    if is_use_with_gocq:
        raw_conf = raw_conf.replace("{is_use_with_gocq}", "true")
        raw_conf = raw_conf.replace("{download_domain}", download_domain)  # type: ignore
        raw_conf = raw_conf.replace("{accounts}", """
    - uin: {uin}
      password: "{password}"
      protocol: {protocol}""".
      format(uin=str(uin), password=password, protocol=str(protocol)))  # type: ignore
    else:
        raw_conf = raw_conf.replace("{is_use_with_gocq}", "false")
        raw_conf = raw_conf.replace("{accounts}", "[]")

    raw_conf = raw_conf.replace("{saucenao_key}", saucenao_key)

    with open(conf_path, "w", encoding="utf-8") as w:
        w.write(raw_conf)
