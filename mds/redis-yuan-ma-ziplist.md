title: Redis源码阅读: ziplist 
tags: 源码阅读,redis
date: 2014-08-08
***
**ziplist**是一个特殊编码的双向链表,能够很高效的使用内存.能够存储`string`和`intege`，其中整数使用实际的二进制
，在两端O(1)复杂度内完成push和pop操作,每一个操作都需要重新分配内存(**realloc**),实际的复杂度跟内存的使用量
有关。

###一.ziplist的结构
ziplist整体结构:
`<zlbytes><zltail><zllen><entry><entry><zlend>`

* `zlbytes`: 是一个非负整数，用来保存整个ziplist的字节长度，是的我们不用遍历获取长度，直接可以重新设置
ziplist的长度.
* `zltail`: ziplist中最后一个entry的偏移量, 方便在尾端进行pop操作. 
* `zllen`: ziplist中entry的数量.
* `zlend`: 等于255的特殊字节，表示ziplist的结束.
***
ziplist entry结构: `<header><data>`

* `header`: header区分为两个部分 
        
    **1)** 前一个entry的长度,使得ziplist能够从后向前遍历, 如果前一个entry的长度小于254字节,只需要一个字节
表示长度；如果一个entry的长度大于或者等于254字节,使用五个字节表示长度，其中第一个字节等于254,后续四个字节
表示实际的长度.
    
    **2)** 数据类型及长度编码
    * |00PPPPPP|: 字符串类型，长度小于等于63 bytes
    * |01PPPPPP|PPPPPPPP|: 字符串类型，长度小于等于16383字节
    * |10PPPPPP|PPPPPPPP|PPPPPPPP|PPPPPPPP|PPPPPPPP|: 字符串类型, 长度大于等于16384字节
    * |11000000|: 整数类型, int16_t
    * |11010000|: 整数类型, int32_t
    * |11100000|: 整数类型, int64_t
    * |11110000|: 整数类型, 24 bit signed
    * |11111110|: 整数类型, 8 bit signed
    * |1111xxxx|: 整数类型, 4 bit integer
    * |11111111|: ziplist的结束符

**以上所有的整数都是使用小端表示**
###二.ziplist操作
待续

