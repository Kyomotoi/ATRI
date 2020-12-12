当前目录：插件列表 > plugin_anime

### 以图搜图

```shell
以图搜图 [pic]
```

- 如发送命令后没附带图片，bot则会向请求者索取图片

### 以图搜番

```shell
以图搜番 [pic]
```

- 如发送命令后没附带图片，bot则会向请求者索取图片

### 涩图

- 使用正则匹配
- 每小时限制索取 5 张
- 涩图源分为 接口（loliconAPI）和 本地（需要自己上传，具体请关注 [plugin_sqlite](modules/plugin_sqlite.md)），修改请见下面

正则表达式：
```
来[点丶张份副个幅][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkd|GKD|搞快点]|[gkd|GKD|搞快点][涩色瑟][图圖]
```

### 涩图源类型

命令：
```shell
/setu-type [type]  # Normal: 2
```

Type:
    - 1  本地数据库
    - 2  loliconAPI（每天限制300次）
