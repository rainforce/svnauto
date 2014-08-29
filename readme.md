多用户多项目的SVN管理系统

特性
自动配置SVN仓库，使用apache管理SVN以及进行校验
用户信息来自mysql，可以与其它项目的用户自由结合
仓库属于用户，一个用户拥有多个仓库

安装
配置
settings.py
SVNROOT, SVNHOST
配置数据库

python manager.py shell
>>from install import install
>>install()

启动WEB服务
python manager.py runserver

使用
创建用户
/users/<>/new/
删除用户
/users/<>/delete/
创建项目
/users/<>/<>/new/
删除项目
/users/<>/<>/delete/
用户列表
/users/
项目列表
/users/<>/
