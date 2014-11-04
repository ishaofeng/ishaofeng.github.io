title: 守护者进程
tags: 读书笔记
date: 2014-11-04
***
###1.介绍
守护者进程是一种生存周期较长的进程，没有控制终端在后台运行，跟随系统启动，系统关闭关闭.
用户层守护者进程缺少控制终端可能是守护进程调用了setsid的结果，所有用户层守护者进程都是
进程组的组长进程以及会话的首进程。

###2.编程规则

1. 调用umask将文件模式创建屏蔽字为0
2. 调用fork,然后使父进程退出
> 1) 如果守护者进程作为一条简单的shell启动,父进程终止使得shell任务这条命令已经结束
> 2) 子进程继承了父进程的进程ID，但具有一个新的进程ID， 保证子进程不是进程组的组长进程
3. 调用setsid以创建一个新会话，使得调用进程产生以下效果
    1. 成为新会话的首进程
    2. 成为一个新进程组的组长进程
    3. 没有控制终端
> 再次进程fork并且使得父进程终止，第二子进程作为守护者进程继续运行，这样保证了该守护者进程不是会话首进程
> 防止它控制终端
4. 将当前目录更改为根目录
5. 关闭不在需要的文件描述符
6. 某些守护者进程需要打开/dev/null使得具有文件描述符0,1和2,使得任何尝试读标准输入,写标准输出或标准出错
的程序都不会产生任何效果


###3.实现代码

    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <signal.h>
    #include <fcntl.h>
    #include <sys/resource.h>
    #include <sys/stat.h>

    void daemonize(const char *cmd)
    {
        //创建文件mask
        umask(0);

        //获取最大文件描述符数
        struct rlimit rl;
        if (getrlimit(RLIMIT_NOFILE, &rl) < 0)
        {
            printf("不能获取最大打开文件数\n");

            exit(-1);
        }

        //成为会话组长,失去控制终端
        int pid;
        if ((pid = fork()) < 0)
        {
            printf("不能创建子进程\n");

            exit(-1);
        }
        else if (pid != 0)
        {
            exit(0);
        }
        setsid();

        //保证为来不获取控制终端
        struct sigaction sa;
        sa.sa_handler = SIG_IGN;
        sigemptyset(&sa.sa_mask);
        sa.sa_flags = 0;
        if (sigaction(SIGHUP, &sa, NULL) < 0)
        {
            printf("不能忽略 SIGHUP\n");
        }

        //第二次fork是的精灵进程不是对话的首进程从而取得终端控制权
        if ((pid=fork()) < 0)
        {
            printf("不能创建子进程\n");

            exit(-1);
        }
        else if (pid != 0)
        {
            exit(0);
        }

        if (chdir("/") < 0)
        {
            printf("不能切换当前目录\n");
            exit(-1);
        }

        if (rl.rlim_max == RLIM_INFINITY)
        {
            rl.rlim_max = 1024;
        }
        int i = 0;
        for (; i < rl.rlim_max; ++i)
        {
            close(i);
        }

        int fd0, fd1, fd2;
        fd0 = open("/dev/null", O_RDWR);
        fd1 = dup(0);
        fd2 = dup(0);
    }

    int main()
    {
        daemonize(NULL);

        sleep(20);

        return 0;
    }
