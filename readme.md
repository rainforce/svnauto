多用户多项目的SVN管理系统
=====================

特性
---
自动配置SVN仓库，使用apache管理SVN以及进行校验用户信息来自mysql，可以与其它项目的用户自由结合仓库属于用户，一个用户拥有多个仓库。
操作接口通过django提供。

安装
---

* 部署django,参见django其它部署文档
* 在settings.py中配置SVNROOT, SVNHOST
* 在settings.py中配置mysql数据库
* 安装httpd svn等环境::

    python manager.py shell
    >>from install import install
    >>install()

* 启动WEB服务::

    python manager.py runserver

使用
---
* 创建用户::

    /users/<USERNAME>/new/
    
* 删除用户::

    /users/<USERNAME>/delete/
* 创建项目::

    /users/<USERNAME>/<PROJECTNAME>/new/
    
* 删除项目

    /users/<USERNAME>/<PROJECTNAME>/delete/

* 用户列表

    /users/

* 项目列表

    /users/<USERNAME>/
