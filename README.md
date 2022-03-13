![](https://socialify.git.ci/Kyomotoi/ATRI/image?description=1&descriptionEditable=A%20project%20for%20ATRI%2C%20Usage%20go-CQHTTP%20%2B%20NoneBot2.&forks=1&issues=1&language=1&logo=https%3A%2F%2Fi.loli.net%2F2020%2F11%2F12%2FYcINCkyp8vK2inD.png&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Light)

# ATRI——一个厨力项目
アトリは、高性能ですから！

[![time tracker](https://wakatime.com/badge/github/Kyomotoi/ATRI.svg)](https://wakatime.com/badge/github/Kyomotoi/ATRI)

[![](https://img.shields.io/github/license/Kyomotoi/ATRI?style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0.html)
[![](https://img.shields.io/badge/QQgroup-567297659-blue?style=for-the-badge)](https://jq.qq.com/?_wv=1027&k=a89kfKQE)

- 文档:
    - [传送门 1](https://atri.kyomotoi.moe)
    - [传送门 2](https://project-atri-docs.vercel.app)

- [更新日志](changelog.md)

## 关于（About）

本项目名称、灵感均来自 [ANIPLEX](https://aniplex-exe.com/) 发行的 [ATRI-My Dear Moments-](https://atri-mdm.com/)

本项目中所使用的任何有关 ATRI 的图标、LOGO，解释权、著作权均归 [ANIPLEX](https://aniplex-exe.com/)。你可以[在此](https://aniplex-exe.com/guidelines/)查看相关内容

为QQ群中复现一个优秀的功能性机器人是本项目的目标

## 声明（Attaction）

**一切开发旨在学习，请勿用于非法用途**

## 实现（Work）

本项目可以在**任何平台**下运行，只要你具备基本的 `Python >= 3.8` 环境和一根接入互联网的网线

实现方式为 `go-cqhttp 或其它遵守Onebot标准的协议` + `NoneBot2`

因项目的特殊性，会不定时进行更新。更新日志：请关注commit

再一个：由于学业原因，在 `2022年6月` 前不会有太大的更新，当然，欢迎提交 `Pull Request`

## 功能概览（Preview）

> 此页面只展示主要功能，详细请在示例群内 **@机器人** 并发送`菜单`以获取帮助

> 如碰到示例机器人未响应，大概率是寄了

- 涩批:
    - 文爱
    - 涩图
    - 涩图嗅探
    - 涩批翻译机

- 实用:
    - 在线运行代码
    - 伪造转发内容
    - 以图搜图
    - 以图搜番
    - ATRI语（加密、解密，改自[`rcnb`](https://github.com/rcnbapp/RCNB.js)）
    - 简单骰子

- 娱乐:
    - 看不懂的笑话
    - 今天吃什么
    - 老婆！

- 其他:
    - B站小程序解析
    - 状态查看

## 使用Docker部署
> 注意，本条目仅为使用docker的部署方法，如果您不知道何为docker，请参考文档中的传统部署方法

> 由于能力有限，默认状态下无法通过环境变量配置bot，请自行修改config.yml 之后再部署
> 同样的，在宿主机直接访问日志等在现阶段也无法做到，请谅解 

> 基于python 3.8，默认使用清华的pip源

获取项目的所有文件之后:

   - 如果你是x86用户:
    
        >sudo docker-composed up

   - 如果您是aarch64 (ARM64) 用户:
    
   由于平台特殊性，请确保在`%ATRI%`目录下存在`tenserflow`的`whl`文件，例如`tensorflow-2.8.0-cp38-none-linux_aarch64.whl`，无需重命名
    
        > cp ./Dockerfile ./Dockerfile_x86 && cp -f ./Dockerfile_aarch64 ./Dockerfile
    
        > sudo docker-composed up

-  对于所有平台，在看到bot成功运行并扫码登陆之后，CTRL + C 结束运行，之后

    >sudo docker-composed up -d

**TODO**:

  - [ ] 网页控制台
  - [ ] RSS订阅
  - [ ] B站动态订阅
  - [ ] 冷重启
  - [ ] 进裙验证（问题可自定义）
  - [ ] 好感度系统（目前优先在[`go-ATRI`](https://github.com/Kyomotoi/go-ATRI)上实现）
  - [ ] 模拟韭菜

## 特别感谢（Thanks）

[Bot Universe](https://github.com/botuniverse): [Onebot标准](https://onebot.dev/)

[Mrs4s](https://github.com/Mrs4s): [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

[NoneBot](https://github.com/nonebot): [NoneBot2](https://github.com/nonebot/nonebot2)

[Richard Chien](https://github.com/richardchien), [Mnixry](https://github.com/mnixry) and GoCQHTTP Dev Group

[JetBrains](https://www.jetbrains.com/?from=ATRI): 为本项目提供 [PyCharm](https://www.jetbrains.com/pycharm/?from=ATRI) 等 IDE 的授权<br>
[<img src="https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/noting/jetbrains-variant-3.png" width="200"/>](https://www.jetbrains.com/?from=ATRI)

以及以下朋友们：
<details markdown='1'><summary>*/ω＼*(</summary>
    *排名不分现后*<br>
    · 50861735 11.00 CNY<br>
    · 1072324725 17.00 CNY<br>
    · AfdianUser_quGy 5.00 CNY<br>
    · 1752179928 56.14 CNY<br>
    · Mikasa 66.00 CNY<br>
    · SkipM4 32.00 CNY<br>
    · Chunk7 33.00 CNY<br>
    · Wwwwwwalnut 10.00 CNY<br>
    · 演变 5.00 CNY<br>
    · 梓哟P 23.33 CNY<br>
    · Ohdmire 20.00 CNY<br>
    · TerRALi 23.45 CNY<br>
    · 虾仁 10.00 CNY<br>
    · Tianli 11.00 CNY
</details>

## 支持（Support）

本项目已启用爱发电，你的支持就是对开发者的最大鼓励！

并会将你的ID写在项目**特别感谢**一栏。

-> https://afdian.net/@Kyomotoi

## 贡献（Contribute）

如果你在运行本项目中发现任何问题，你可以：

- [提交 Issue](https://github.com/Kyomotoi/ATRI/issues)
- [提交 Pull request](https://github.com/Kyomotoi/ATRI/pulls)
- [在反馈群内进行反馈](https://jq.qq.com/?_wv=1027&k=WoAAYXbJ)


- 提交 `Pull request` 时，请注意：

    - 所提交的代码尽量与原仓库代码风格保持一致
    - 遵守 [`PEP-8`](https://www.python.org/dev/peps/pep-0008/) 标准
    - 变量名清晰明了
    - 包含单元测试（对插件的修改/添加）
    
    如果你是初次提交 `Pull request`，请先阅读[这篇文章](https://atri.kyomotoi.moe/developer/overview/)

## 协议（License）

本项目使用 [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) 协议

意味着你可以运行本项目，并向你的用户提供服务，但出现对本项目源码进行修改，则需要将你修改后的版本对你的用户`开源`

在运行本项目期间，行为违反当地法律法规的而被处理的，本项目概不承担任何责任
