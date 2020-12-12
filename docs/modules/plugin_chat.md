当前目录：插件列表 > plugin_chat

### 关键词学习

!> 此功能仍需等待完善，目前仅支持维护者添加关键词

命令：
```shell
/learnrepo [key] [repo] [proba]  #添加关键词，普通用户添加进入审核列表
/learnrepo review  #审核关键词
/learnrepo del [key]  #删除关键词
```

参数类型：
```
    * key: 关键词(将使用遍历匹配)
    * repo: 触发后的关键词
    * proba: 回复机率，示例：1 = 100%，2 = 50%，3 = 33.3%...
```

### 好友 / 群 请求处理

- 旨在代替人工同意他人的 添加 / 邀请

命令：
```shell
/selfevent [type]-true/false  #Normal: false
```

参数类型：
```
    * type: group / friend
```

### 戳一戳

- 代替双击头像戳一戳bot
- 也可在聊天中双击bot头像以触发

命令：
```shell
@bot 戳一戳
```

### 口臭一下

- 口臭请求者

命令：
```shell
@bot 骂我/口臭/口臭一下
```

### 一言

- 安慰/鼓励一下请求者

命令：
```shell
@bot 一言/抑郁一下/网抑云
```

### 来句笑话

- 以请求者的 ID 代入至笑话中

命令：
```shell
来句笑话
```

### 漂流瓶

- 神奇的小瓶子装了一个世界

命令：
```shell
@bot 扔漂流瓶
@bot 捞漂流瓶
清除漂流瓶  #仅限维护者
```
