title: pyquery学习
tags: python
date: 2014-10-28
***
###简介
最近在做geeksforgeeks.org上面的题，上面不能记录哪个已经学习了哪个还没有学习，想把上面的题目爬下来这样方便记录哪些已经学习了，之前尝试过pyquery,今天根据文档学习一下然后用用，pyquery允许我们使用jquery的语法进行xml和html文档的操作，它使用lxml作为底层因而速度非常块。

    安装 sudo pip install pyquery
    使用 from pyquery import PyQuery as pq
    
###**1.载入文档**

1. 字符串文档: `doc = pq("<html></html>")`
2. 从网址打开: `doc = pq(url="http://www.baidu.com")`
    
    下载文档默认使用的是urllib, 如果安装了requests则直接使用requests， 并且可以使用requests中的大多数参数

3. 从网址打开指定获取网页内容的方法:`doc = pq(url="http://www.baidu.com",opener=lambda url, **kw: requests.get(url).text)`
4. 从本地文件打开:`doc=pq(filename=filepath)`

###**2.属性**

    doc = pq('<p id="p1" class="style1"><p id="p2" class="style2">嵌套层</p></p><p id="p3" class="style3">兄弟层</p>')
    #获取所有p
    ps = doc("p")
    *[<p#p1>, <p#p2>, <p#p3>]*
    #获取属性，默认使用第一个标签项
    print ps.attr.id  #p1
    print ps.attr("id")
    print ps.eq(1).attr.id #p2
    #设置属性
    ps.attr.id = "ps4" #将更改所有标签的id为ps4
    ps.attr("id") = "ps4"

###**3.CSS**

    #添加一个class
    p.addClass("toto")
    #两个class之间切换
    p.toggleClass("toto titi")
    #删除class
    p.removeClass("titi")
    
    #设置css属性
    p.css.font_size = "16px"
    #获取所有的css
    p.attr.style

###**4.操作**

    p = pq('<p id="test"> ###### </p>')
    
    #**在标签内容最后加入**
    p.append('test <a href="http://www.baidu.com"></a>')
    #结果>>>u' ###### test <a href="http://www.baidu.com"/>'
    
    #**在标签内容前面添加**
    p.prepend("test<a href="http://www.baidu.com"></a>')
    #结果>>>'test<a href="http://www.baidu.com"/> ######  '
    
    #**添加一个标签到另一个内容之前**
    p.appendTo(d("#test"))
    
    #**添加一个标签到另一个内容之后**
    p.prependTo(d("#test"))
    
    #**添加一个标签到另一个之前**
    p.insertBefore(d("#test"))
    
    #**添加一个标签到另一个之后**
    p.insertAfter(d("#test"))
    
    #**迭代对标签本身进行处理**
    p.each(lambda e: e.addClass("hello2"))
    
    #**迭代处理生成新的列表**
    p.map(lambda e: e.text())
    
    #**删除一个标签**
    p.remove("p#id3")
    
    #**清空一个标签内的内容**
    p.empty()
    
    #**检测一个标签是否复合要求**
    p.is_(".test")
    
    #**生成一个迭代生成器**
    for item in p.items():
        print item.text()
    
###**5.遍历**

    #选定一个指定的标签
    d.eq(0)
    
    #查找嵌套标签
    d.find("a")
    
    #查找嵌套标签并返回其父标签
    d.find("a").end()
    
    #过滤标签
    d.filter("a")

