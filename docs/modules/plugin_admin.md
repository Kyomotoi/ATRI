当前目录：插件列表 > plugin_admin

!> 此插件下的所有命令普通用户无权使用

### 模块控制

命令：
```shell
/switch on/off-{service}  #单独控制群聊，群管理、维护者可用
/switch all-on/off-{service}  #控制全局，仅维护者可用
```

各个可控模块名称：
```
    plugin_anime:
        anime-pic-search  #以图搜图
        anime-vid-search  #以图搜番
        anime-setu  #涩图
    
    plugin_chat:
        drifting-bottle  #漂流瓶
        
    plugin_pixiv:
        pixiv-pic-search  #p站图片搜索
        pixiv-author-search  #p站作者搜索
        pixiv-rank  #p站排行榜
        
    plugin_utils:
        one-key-adult  #虚拟身份证
        genshin-search  #原神战绩查询
```

demo：
```shell
/switch on-anime-setu  #此处的 anime-setu 即模块名（service）。
```

### 舆情监控

命令：
```shell
/pubopin [key] [repo] [times] [ban time(bot)]  #添加监控关键词
/pubopin del [key]  #删除关键词
/pubopin list  #列出启用关键词
```

参数类型：
```
    * key: 关键词(将使用正则匹配)
    * repo: 触发后的关键词(可选)，如为图片，键入 img
    * times: 容忍次数(n>0, int)
    * ban time: bot对其失效时间(min, int)
```

demo：
```shell
/pubopin test testrepo 233 114514
```

### 错误堆栈追踪

命令：
```shell
/track [trackID]  #此处的 trackID 为功能在运行时发生错误所返回的错误追踪码
```

错误返回示例：
```
   ERROR! Reason: [请求数据失败，也可能为接口调用次数达上限]  #此处为大致的错误引发原因
   trackID: McZNWjbI132r5DXl  #此处即为错误码返回
   请使用[来杯红茶]功能以联系维护者
   并附上 trackID
```

demo：
```shell
/track McZNWjbI132r5DXl
```

### 群发

命令：
```shell
/groupsend [Message]
```

返回示例：
```
    推送信息：
    Message
    ————————
    总共：n
    成功推送：n
    失败[0]个：
    #推送失败的群会在此列出
```
