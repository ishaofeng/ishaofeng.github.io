title: 高质量Python读书笔记
tags: python,读书笔记
date: 2014-09-13
***
####1.字符串格式化

    #一般方式格式化(我大部分这么写的)
    print 'Hello %s!' % ('Tom', ) 

    #pythonic方式
    value = {"greet": "hello world", "language": "Python"}
    print "%(greet)s from %(language)s" % value

    #more pythonic方式
    print '{0} from {1}'.format("hello world", "Python")
    print '{greet} from {language}'.format(**value)
    print '{greet} from {language}'.format(greet="hello world", language="Python")
    print '{score:0.3}'.format(score=45.422342)

上述的格式化方法以前都见过学习过，但是习惯使然，大部分情况下我都使用的
第一种，其实后面两种在复杂格式化中很方便并且清晰明了，比如一个格式化中
某个值要多次出现，书上说最后一种是python最推荐的方式


####2.switch...case的替代方案
c,c++或者java中的switch case在python中没有直接支持，一般使用的时候都是
使用多个if..elif..else关系替换，在这本书上看到一个替代方式感觉蛮好，在
以上支持swtich case的语言中switch case与if..else...最大的不同是前者是一步
定位后者是逐步比较，下述代码说明了python上的替代方式，使用字典完成

    def f(x):
        return {
            0: "you typed zero.\n",
            1: "you are in top.\n",
            2: "n is event number.\n"
        }.get(n. "only single-digit numbers are allowed\n")

####3.Python的常量
Python使用常量的方式书上列出了两种方式:
* 通过命名方式，常量名所有字母大写并且各个单词之间使用下划线连接
* 通过自定义的类实现常量功能,满足**命名全部为大写**和**值一旦绑定
便不可再修改**这两个条件，下面代码是作者列出的一个实现

    class _const:
        class ConstError(TypeError): pass
        class ConstCastError(ConstError): pass

        def __setattr__(self, name, value):
            if name in self.__dict__:
                raise self.ConstError, "Can't change const %s" % name
            
            if not name.isupper():
                raise self.ConstCastError,  \
                    'const name "%s" is not all uppercase' % name

            self.__dict__[name] = value
    
    import sys
    sys.modules[__name__] = _const()

> 一般干活的时候都使用的是第一种，因为在其它语言中我们一般是通过命名的方式
> 弄到，但是我用的那些语言都支持const关键字或者类似的关键字，通过作者
> 提供的第二种方式能够避免，常变量错误修改

####4.改变默认字符编码
python２.7x中的默认编码是ascii编码,设置编码的方式有很多中这里说说

1. 在代码文件之前执行选项之后加入`#encoding=utf8`,　这样文件中如果
中文就可以执行
2. 上述设置，如果你从文件中读取汉字的化还是会出错，所以我一般在牵涉
中文字符串处理的代码的文件中添加如下代码，改变默认编码


    import sys
    reload(sys)
    sys.setdefaultencoding("utf8")

说到这里我得提一件事情，之前研一的时候和同学参加腾讯QRobot机器人编程
大赛，我们的后台是使用python写的，在我们这边几个环境中都妥妥的，腾讯
的人说我们的代码在他们那边一直有乱码，饮恨到现在，呜呜, 还么有想清楚
为什么在这边多个系统中都是妥妥的.
3. 在python3.0之后默认的编码已经变为unicode,而在2.7x中可以使用`from __future__import unicode_literals`
使用这项功能.

**上述三种方式中第三种显然最好，当然最最好的是转向python3.0以后的版本**

####5. 作用域
python的作用域有三种

* 局部作用域
每一个函数调用都会创建一个本地作用域对应locals()
* 全局作用域
定义在Pyhton模块文件中的变量拥有全局作用域对应于globals()
* 嵌套作用域
    存在多层函数嵌套, **在嵌套作用域情况下，如果想在嵌套的行数内修改外
层定义的变量,即使使用global进行申明也不能达到目的，其最终是在嵌套函数
所在的命名空间创建一个新的变量.这种情况只会出现在嵌套情况下**
* 内置作用域
    对应标准库中__builtin_的模块实现
***
名字查找顺序(LEGB法则):
1. 局部作用域
2. 嵌套作用域
3. 全局作用域
4. 内置作用域

####6. 多继承
在多继承中多个基类有相同的方法，到底调用哪一个方法，由相应的方法解析顺序
(MRO)决定

* 古典类: MRO搜索采用简单的自左向右的深度优先方法，即按照类的申明顺序形成
继承树
* 新式类: C3 MRO (貌似还蛮麻烦的, 多数情况下不建议这样继承类)

