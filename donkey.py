#! /usr/bin/python
#encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from jinja2 import *
from datetime import datetime
import os
import markdown
import operator

root_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
env = Environment(loader=FileSystemLoader(os.path.join(root_dir, "views")),
                  block_start_string="[%", block_end_string="%]", variable_start_string="[[", variable_end_string="]]")

def view(templatepath, info):
    return env.get_template(templatepath).render(info)

#custom filters
def timetomonth(t):
    return datetime.fromtimestamp(float(t)).month
env.filters["timetomonth"] = timetomonth

def timetoday(t):
    return datetime.fromtimestamp(float(t)).day
env.filters["timetoday"] = timetoday

conf = {
    "title": u"小毛驴|Coding World",
    "fulltitle": u"小毛驴",
    "keywords": "Linux,Python,Vim,Hadoop,Redis,大数据,跑步",
    "description": "小毛驴CodingWorld, 记录一个Coder的成长",
    "domain": "www.smalllv.cn"
}

if len(sys.argv) >= 2 and sys.argv[1] == "local":
    conf["domain"] = "127.0.0.1:8000"

#解析页面
def parserPage(page):
    with open(page, "r") as f:
        f.readline()
        titleline = f.readline()

        #解析文章元信息
        title = titleline.split(":")[1].strip("# \n")

        content = "##%s\n" % title
        content += f.read()

        #转换文章
        content = markdown.markdown(content)

        return {
                "title": "关于我",
                "content": content,
                "url": "/about.html"}

#解析文档
def parserMds():
    mdpath = root_dir + "mds"
    mds = os.listdir(mdpath)
    mds = [(mdpath + "/" + md, "/posts/%s.html" % md.split(".")[0]) for md in mds]

    posts = []
    for md in mds:
        with open(md[0], "r") as f:
            titleline = f.readline()
            if "page" not in titleline:
                tagline = f.readline()
                dateline = f.readline()

                #解析文章元信息
                title = titleline.split(":")[1].strip("# \n")
                tags = tagline.split(":")[1].strip("# \n").split(",")
                date = dateline.split(":")[1].strip("# \n")

                content = "##%s\n" % title
                content += f.read()

                #转换文章
                content = markdown.markdown(content)
                posts.append({
                    "title": title,
                    "tags": tags,
                    "content": content,
                    "date": date,
                    "url": md[1]
                })

    #对文章按照时间排序
    def postcmp(p1, p2):
        if p1["date"] > p2["date"]:
            return 1
        elif p1["date"] < p2["date"]:
            return -1
        else:
            return 0

    sortposts = sorted(posts, cmp=postcmp, reverse=True)

    #获取tags列表
    tags = {}
    for i, post in enumerate(sortposts):
        for tag in post["tags"]:
            print tag
            if tag not in tags:
                tags[tag] = {}
                tags[tag]["posts"] = []
                tags[tag]["url"] = "/tags/%s.html" % tag
                tags[tag]["title"] = tag

            tags[tag]["posts"].append(i)

    tags = tags.values()

    #对tags根据数量排序
    def tagcmp(t1, t2):
        lt1 = len(t1["posts"])
        lt2 = len(t2["posts"])

        if lt1 > lt2:
            return 1
        elif lt1 < lt2:
            return -1
        else:
            return 0

    sorttags = sorted(tags, cmp=tagcmp, reverse=True)
    print sorttags


    return (tags, sortposts)

if __name__ == "__main__":
    tags, posts = parserMds()
    conf["posts"] = posts
    conf["tags"] = tags
    content = view("index.html", conf)

    #生成文章页面
    for post in posts:
       conf["post"] = post
       postHtml = view("post.html", conf)
       with open(".%s" % post["url"], "w") as f:
           f.write(postHtml)

    #生成分类页面
    for tag in tags:
       tagposts = []
       for postindex in tag["posts"]:
           tagposts.append(posts[postindex])

       conf["posts"] = tagposts
       conf["tag"] = tag
       tagHtml = view("index.html", conf)
       with open(".%s" % tag["url"], "w") as f:
           f.write(tagHtml)

    #生成about页面
    aboutPost = parserPage("./mds/about.md")
    conf["post"] = aboutPost
    aboutHtml = view("post.html", conf)
    with open("./about.html", "w") as f:
        f.write(aboutHtml)

    with open("index.html", "w") as f:
        f.write(content)
