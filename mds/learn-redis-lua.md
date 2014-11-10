title: Redis的Lua脚本
tags: redis
date: 2014-11-10
***
EVAL和EVALSHA是使用Redis内置的Lua解释器执行脚本

**EVAL:**

`eval script argcount arg1 arg2 extraarg1 extraarg2`

* script是eval要运行的脚本，这里的脚本仅仅是程序不包含函数结构
* argcount表示脚本参数的个数, 参数使用`KEYS[index]`, index>0
* 除过argcount表示的参数以外额外的参数使用`ARGV[index]`获取

示例:
```
>eval "return {KEYS[1],KEYS[2],ARGV[1],ARGV[2]}" 2 key1 key2 first second
1) "key1"
2) "key2"
3) "first"
4) "second"
eval的执行结果被转换为Redis命令执行的类型
```

**Lua:**
#####1.调用

* redis.call()
* redis.pcall()
* redis.error_reply(error_string): 从脚本中返回错误
* redis.status_reply(status_string): 从脚本中返回返回状态
* redis.log(loglevel, message): 发送redis的log日志
	* redis.LOG_DEBUG
    * redis.LOG_VERBOSE
    * redis.LOG_NOTICE
    * redis.LOG_WARING

Redis命名的一个字段就是一个参数比如`redis.call('set','foo', 'bar')`

redis.call()在执行失败的时候直接跳异常，终端脚本执行而redis.pcall()则以错误码的形式返回

EVAL的脚本中使用的所有KEY都必须使用KEYS传入，使用Redis能够评估对某个KEY能够执行什么操作

#####2.类型转换
脚本中执行命令的结果将转化为Lua的数据类型，脚本执行完返回的数据将转化为Redis协议值

**Redis数据转化为Lua数据:**
* integer reply -> number
* bulk reply -> string
* multi bulk reply -> table
* status reply -> 只包含OK域的table
* err reply -> 只包含ERR域的table
* Nil reply -> boolean (false)

**Lua数据转化为Redis数据:**
刚好与上述过程反向, Lua的true将转化为1

**Lua数据的特点:**
* Lua中表示数据的数据类型既能表示整数又能表示浮点数，在将Lua的integer返回值移除浮点数部分，如果确实要从脚本中返回一个浮点数，那么使用字符段返回
* 当Redis将一个Lua数组转化为Redis协议时，如果遇到Nil则停止

#####3.原子性
Redis本身特点:同一时刻仅处理一个请求，使得Redis能够保证脚本以原子的方式执行，在这个过程中没有其它的脚本或者命令能够执行。脚本中命令的执行和事物效果类似，
> 原子性的优点也是一个缺点，在脚本执行过程中Redis不能响应其它客户端的命令请求，因而脚本本身执行不能处理大量任务应该尽可能快的完成

#####4.函数特性
* 脚本在AOF或者是主从复制时直接发送脚本
* Lua不能使用命令访问外部时间或者外部状态
* 如果在一个随机命令之后有一个改变数据的命令执行,Redis将用一个错误阻止脚本继续执行
* Redis中存在返回元素顺序随机的命令，但是这些命令在Lua中执行返回的顺序是一致的
* 同一个脚本调用Lua的`math.random`生成的随机数顺序总是一致的(`math.randomseed`不被改变的情况下
* 脚本中不能存在全局变量,所有生命的变量建议以local关键字
* 脚本只能够操作Redis数据和传入的参数

#####5.可用的Lua库
#####5.1 struct
与python的struct库非常类似支持类型有:
```
> 大端表示
< 小端表示
![num] 对齐
x 占位
b/B signed/unsigned byte
h/H signed/unsigned short
l/L signed/unsigned long
T size_t
i/In signed/unsiged integer with size n(默认是int的长度)
s zero-terminated string
f float
d double
```
操作:
```
1) 将连个short打包
> eval 'return struct.pack('HH', 1, 2)' 0
2) 解包
> eval 'return {struct.pack('HH', ARGV[1])}' 0 "\0x01\x00\x02\x00"
3) 获取给定结构的长度
> eval 'return struct.size("HH")' 0
4）不能直接获取s的操作
```
python中的struct能够直接设定元素的个数，此处的struct貌似没有

#####5.2 cjson
```
> eval 'return cjson.encode({["foo"]="bar"})' 0
> eval 'return cjson.decode(ARGV[1])["foo")["foo"]' 0 "{\"foo\":\"bar\"}"
```
######5.3 cmsgpack
```
> eval 'return cmsgpack.pack({"foo", "bar", "baz"})' 0
> eval ' return cmsgpack.unpack(ARGV[1])' 0 ....
```
######5.4 redis.sha1hex 
```
> eval 'return redis.sha1hex(ARGV[1])' 0 "FOO"
SHA1 RESULT
```
**脚本处理:**
* 使用EVAl重复执行相同的脚本，Redis会对编译后的脚本进行缓存，一个已经执行的脚本将保证被缓存在其运行的Redis实例上
* 缓存的脚本就像一条新的命令一样，并且一个应用中脚本的数量总是很有限的，缓存本身并不消耗太多内存
* `SCRIPT FLUSH`能够清空Redis中的脚本缓存
* `SCRIPT LOAD`加载一个脚本到脚本缓存中
* `SCRIPT EXISTS sha1 sha2`检测脚本列表中的脚本是否存在
* `SCRIPT KILL`杀死运行时间到达配置文件脚本最大运行时间的脚本

**EVALSHA:**
使用EVAl执行相同的脚本需要重复发送相同的内容，EVALSHA是用来避免对相同脚本重复发送的问题，EVALSHA第一个参数是要执行的脚本的SHA1值,如果响应脚本存在则直接执行，如果脚本不存在则返回一个特殊的错误告诉客户端使用EVAL执行

**注意:**
* 默认情况下脚本的最长执行时间为5s,可以通过设置`lua-time-limit`设置
* 当脚本运行超时时，将开始接受其它客户端的命令,并且仅接收`SCRIPT KILL`	和`SHUTDOWN NOSAVE`命令, 前一个命令能够终止不写命令的脚本, 后一个直接终止服务器并且不保存数据
* 在Pipeline环境中建议使用eval
* 在Pipeline中如果有evalsha则在Pipeline环境初始化之前检测响应的脚本是否存在，如果不存在使用`SCRIPT LOAD`加载脚本




参考: http://www.redis.io/commands/eval
