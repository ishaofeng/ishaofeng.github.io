title: 使用Python下载多看电子书
tags: python,工具
date: 2014-08-02
***
这两天**多看**(ps:必须说现在多看做的越来越Kindle了)电子书免费看三天，昨天看到微博有人提取了文字，有人说不能保存格式，那么问什么不直接截图呢，
所以就写了写，下载了四本书，么有体力继续了哈哈， 之前用过`selenium`东东，用的时候发现Chrome上还是不
太稳定,不折腾这个了。
    
使用它`python duokan.py 图书网页id  书名  起始页码`当浏览器打开后,调整合适的尺寸，然后任意输入就
可以开始啦，速度稍微有那么一点点慢，但是下载还是妥妥的，我和小伙伴都这么搞了，中间可能会弹出活动
提示，在打开图书的时候直接往后拖拽,这个只弹出一次，然后再拖拽回去就不会再出现了.
    
    #! /usr/bin/python
    #coding=utf-8

    from selenium import webdriver
    import time

    import sys

    import os

    url=sys.argv[1]
    name=sys.argv[2]
    start=int(sys.argv[3])

    if os.path.exists(name) == False:
        os.mkdir(name)

    browser = webdriver.Chrome()
    browser.set_window_size(600, 800)
    browser.get(url)

    wait = raw_input("请重置尺寸后开始>>")

    pageCount = browser.execute_script("return $('.j-md-footer .left').html().split('/')[1]; ")
    pageCount = int(pageCount)
    time.sleep(2)
    for i in xrange(start, pageCount):
        print "保存页面 ", i
        browser.execute_script("$('.j-pagedown').click()")
        c = 6
        time.sleep(2)

        browser.execute_script("var btn = $('.u-layer #activity_tip_dialog').parent().css('display') == 'none'; if (btn) { \
                    $('.u-btn.j-close').click()}")


        print browser.save_screenshot("./%s/%s_%05d" % (name, name, i))

