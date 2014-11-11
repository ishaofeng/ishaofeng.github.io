title: epoll的基本概念
tags: redis
date: 2014-11-11
***
select/poll/epoll多路复用功能顺序增强,select最大打开文件数限制FD_SETSIZE默认是1024,并且进行更改还很麻烦,epoll的最大限制取决于系统内存,对于大量连接,FD数量特别大，但是同一时间内活跃的socket很少，select/poll每次调用都需要线性扫描集合，因而性能会随着FD的增加而线性降低

**poll vs select:**
* select()使用fd_set传入要监控的事件，因而每一次循环需要拷贝fd_set,而poll传入一次时间数组可以一直使用
* poll()能够处理更多的文件描述符,而select()最多能够处理1024个(通过重新编译能够支持大于1023)
* poll()的超时使用的是毫秒，而select的超时使用的是`struct timeval`精度更高
* 都是使用线性的方式处理文件描述符,处理的描述符越多速度越慢

epoll只对活跃的socket进行操作

**epoll工作方式: LT, ET**

* LT: 默认模式，支持阻塞和非阻塞socket, 内核通知一个描述符就绪，如果不进行处理还会继续通知。水平触发。
* ET: 高速模式, 只支持非阻塞socket,从描述符未就绪变为就绪,内核通知这个描述符就绪，如果已经通知你知道了，则不会再为那个文件描述符发送就绪通知，直到响应描述符状态发生改变。边缘触发。


**注意:**来自内核的可读通知仅仅是有可读的可能，如果文件描述符还没有就绪，但是收到了来自内核的通知如果这个时候去读对于阻塞socket那么当前读操作将会阻塞，因而在使用可读通知事件时使用非阻塞模式的socket

**接口:**
* 头文件`#include <sys/epoll.h>`
* epoll_create: 创建一个epoll文件描述符
```
//maxfds是epoll所支持的句柄数
int epoll_create(int size);
```
* epoll_ctl: 用来添加或者删除需要侦听的文件描述符及其事件
```
//epfd是epoll_create的返回值
//op表示动作:
//		EPOLL_CTRL_ADD: 注册新的fd
//		EPOLL_CTRL_MOD： 修改已经注册的
//		EPOLL_CTRL_DEL: 删除一个注册的fd
//fd表示需要监听的描述符
//event表示要监听的事件
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
//epoll_event结构
typedef union epoll_data
{
	void *ptr;
   	int fd;
    __uint32_t u32;
    __uint64_t u64;
} epoll_data_t;
struct epoll_event
{
	__uint32_t events;
	epoll_data_t data;
}
```
struct epoll_event中的events是下列的宏的集合:
	* EPOLLIN: 文件描述符可读
    * EPOLLOUT: 文件描述符可写
    * EPOLLPRI: 文件描述符有带外数据到来
    * EPOLLERR: 文件描述符发生错误
    * EPOLLHUP: 文件描述符挂断
    * EPOLLLET: 将EPOLL设置为边缘触发模式
    * EPOLLONESHOT: 只监听一次事件
* epoll_wait/epoll_pwait: 接受发生在被侦听的描述符上用户感兴趣的事件
```
//events从内核中得到的时间集合
//maxevents告诉内核这个events最大为多大，不能大于epoll_create的size
//timeout表示超时时间（毫秒), 0表示立即返回，-1永久阻塞
//返回值表示需要处理的时间数目，0表示已经超时
int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);
```
* close: 关闭epoll文件描述符，任何被侦听的文件描述符被删除后相应的也会被从被侦听的文件描述符集合中删除，**自动删除**

**参考:**
* [poll vs select vs event-based](http://daniel.haxx.se/docs/poll-vs-select.html)
* [The C10K problem](http://www.kegel.com/c10k.html)
