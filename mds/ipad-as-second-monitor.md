title: 使用Ipad作为ubuntu的扩展屏幕
tags: 工具
date: 2014-09-12
***
使用自己笔记本再写代码的的时候总是觉得屏幕不够用，在实验室的时候我直接连接一个显示器，虽然屏幕是扩展了一天下来自己脸受不了总是感觉疼的(Ps:做码农
真苦逼). 所以一直想用自己的pad做一个小的扩展，其实很多时候有这么一个小的扩展已经足够啦。在网上找了很长时间发现现成可用的屏幕扩展的方法都是使用
付费软件，并且大部分只能支持mac或者windows, 最终在神奇的google的帮助下找到了这个折中的办法，虽然没有直接再连接一个显示器那么方便，但是已经能够很
大程度上解决我的问题了。

###1. 安装synergy
[Synergy](http://synergy-project.org)是一个能够在多台计算机之间共享鼠标和键盘的免费软件，这个软件是一个免费软件，能够同时支持linux,windows,mac
以前在实验室的时候使用这个软件把自己笔记本和实验室的电脑一起控制，另外还有人把这个软件还移植到android上面了。

安装好以后在系统菜单启动或者使用 nohup synergy & 启动,然后选择配置服务器,在界面上拖动小电脑如下图命名

![synergyconfig](/img/synergyconfig.png)

其中`shaopc`是我的电脑, `left`表示ipad, 你可以按照爱好选择方式则位置

###2. 安装vnc
执行如下命令安装vncserver

    sudo apt-get install vnc4server xvnc4viewer   #安装软件
    vnc4server :1                                 #创建端口号为5901的远程访问桌面
    vncviewer :1                                  #访问远程桌面， 密码使用vncpasswd设置

我们将创建的远程桌面访问到的桌面成为left

###3. 安装tmux
tmux是用来在终端分屏的软件，这里安装tmux主要是为了让ipad方面的桌面和电脑显示的桌面共用一个终端

    sudo apt-get install tmux                     #安装软件
    tmux -S /tmp/share                            #在电脑的终端中执行 
    tmux -S /tmp/share attach                     #在远程桌面中打开的终端执行

在这一步执行完成后我们发现，远程桌面和我们电脑桌面上的终端信息是同步的, 我们交互的是同一个终端会话

###4. ipad中安装vnc
在ipad中安装vnc, 直接在app store中搜索vnc直接进行安装即可， 如果电脑使用的是无线网那么直接让ipad也连接无线网，
否则使用笔记本创建无线网然后ipad连接。

进行如下配置:

1. 打开安装好的vnc软件
2. 添加连接 地址写 主机ip:5901, 名字写ipad
3. 直接连接如果需要密码输入vncpasswd创建的密码
4. 以上步骤完成以后就可以进入第一步创建的桌面, 但是此时键盘和鼠标还是不能共享
5. 在远程桌面中打开一个新的终端输入 `synergyc --name left localhost`
6. 此时鼠标和键盘就可以共享了, 按照之前配置的方向从主机屏幕边缘拖出即可计入ipad访问的桌面


###Over
使用中发现, 有时候鼠标在远程桌面中看不见，可以直接在本机打开一个远程桌面进行操作，平时在远程桌面
中只打开终端，然后在synergy中配置快捷键，方便的在两个屏幕之间进行切换.我还会继续摸索怎么方便的使用.

最终的效果:
![ipadubuntu](/img/ubuntuipad.png)