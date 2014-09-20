title: github.js使用
tags: Web技术
date: 2014-09-13
***
**github.js**是对github v3接口的一个javascript库, 这个库是prose.io的人创建的，
prose.io是一个在线对github上内容进行编辑的网站(ps:界面很简洁使用很方便),github
本身的api接口非常简洁是学习api设计的好的范本,我在这是把github.js的接口使用一遍.

###1. 登陆
Github的api调用认证方式有两种:
* 一种是使用传统的basic认证的方式

    var github = new Github({
        username: "USERNAME",
        password: "PASSWORD",
        auth: "basic"
    })

这种方式虽然使用简单但是存在一定的安全问题，但对于自己博客来说使用这种方式
还是可行的。

* 另一种是oauth2.0认证使用token的方式
    
    var github = new Github({
        token: "TOKEN",
        auth: "oauth"
    })

token本身分为两种一种是自己手动生成的用户个人访问token, 另一种是对授权应用的token

###2. Repo API
* 获取repo   `var repo = github.getRepo(username, reponame)`
* 显示repo的信息 `repo.show(function(err, repo) {})`
* 获取指定路径的内容 `repo.contents(branch, "path/to/dir", function(err, contents){}, sync)`
* fork一个repo `repo.fork(function(err) {})`
* 创建新的分支  `repo.branch(oldBranchName, newBranchName, function(err){})`
* 列出所有分支 `repo.listBranches(function(err, branches){})`
* 在指定路径存储内容 `repo.write("master", "path/to/file", "NEW_CONTENTS", \
        "COMMIT_MESSAGE", function(err){})`
* 读取指定路径内容 `repo.read("master", "path/to/file", function(err, data){})`
* 移动文件 `repo.move("master", "path/to/file", "path/to/new_file", function(err){})`
* 删除文件 `repo.remove("master", "path/to/file", function(err){})`
* 访问repo的根路径的文件　`repo.getTree("master", function(err, tree){})`
* 递归访问repo的的所有文件 `repo.getTree("master?recursive=true", function(err, tree){})`
* 给定一个文件路径获取响应的blob或tree的sha `repo.getSha("master", "/path/to/file", function(err, sha){})`

