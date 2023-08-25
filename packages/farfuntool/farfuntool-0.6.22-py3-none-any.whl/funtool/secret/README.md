# 简介

> 经常用到一些账号，密码，token之类的数据  
> 不适合直接写死在代码中，不便修改
> 代码需要提交到代码库，不适合账号密码同步过去

1.本地：密码保存在本地，默认在`~/.secret/secret.db`  
2.无明确含义：应用场景独立配置key，如百度登录账号，可保存为`read_secret("bd", "bt", "uid", value="account")`，单独拿到这些信息，也不知道`value`
是干嘛的，需要配合代码才能知道`value`
是具体什么账号/密码  
3.可加密：`value`可支持`加密解密`

# 使用场景

### 普通账号、密码类的保存读取

```python
from notetool.secret import read_secret

# 保存
user_id = read_secret("baidu", "bingtao", "user_id", value="account")

# 读取
user_id = read_secret("baidu", "bingtao", "user_id")
```

### 带过期时间的保存读取

有些平台的token的有效期是2小时，2小时后需要重新获取

```python
from notetool.secret import read_secret

# 保存
user_id = read_secret("baidu", "bingtao", "user_id", value="account", expire_time=3600)

# 读取
user_id = read_secret("baidu", "bingtao", "user_id")
```

### 带加密的保存读取

```python
from notetool.secret import read_secret

# 保存
user_id = read_secret("baidu", "bingtao", "user_id", value="account", expire_time=3600, secret='this is secret key')

# 读取
user_id = read_secret("baidu", "bingtao", "user_id", secret='this is secret key')
```