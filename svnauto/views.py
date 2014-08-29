
#*-* coding:utf-8 *-*
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os, shutil

from pwd import getpwnam

def _write_from_tpl(tpl, context, target):
    """使用模板写配置文件
    """
    t = get_template(tpl)
    content = t.render(context)
    
    with open(target, 'w+') as f:
        f.write(content);
        
        
def _chown2(dir,uid,gid):
    for f in os.listdir(dir):
        if os.path.isdir(f):
            _chown2(f)
        else:
            os.chown(f, uid, gid)

def _chown(dir, user):
#     uid,gid = getpwnam(user).pw_uid,getpwnam(user).pw_gid
#     _chown2(dir, uid, gid)
    os.system("chown -R {u}.{u} {d}".format(u=user,d=dir))

def _sucess(request):
    return render(request, 'ajax.json', {'result':'sucess'})

def _fail(request):
    return render(request, 'ajax.json', {'result':'failed'})

def install(request):
    '''部署SVN环境
    '''
#     make dirs
    ROOT = settings.SVNROOT
    HTTPD_CONF = settings.HTTPD_CONF
    
    path = os.path.join(ROOT, 'httpd/system/')
    if not os.path.exists(path):
        os.makedirs();
#     create config file
    db_settings = settings.DATABASES['default'];
    mysql_context = Context({
                             "db":db_settings['NAME'],
                             "user":db_settings['USER'],
                             'host':db_settings['HOST'], 
                             "passwd":db_settings['PASSWORD']
                             })
    
    _write_from_tpl('mysql.conf', mysql_context, os.path.join(ROOT, 'httpd/system/mysql.conf'))
    _write_from_tpl('svn_mysql.conf', Context({}), os.path.join(ROOT, 'httpd/system/svn_mysql.conf'))
    os.system("yum install httpd mod_dav_svn mysql-devel apr-util-mysql svn mod_dav_svn")
#     midify httpd config
    with open(HTTPD_CONF, 'a') as f:
        f.write('\nInclude ' + os.path.join(ROOT, 'httpd/system/mysql.conf'))
        f.write('\nInclude ' + os.path.join(ROOT, 'httpd/*.conf'))
        
    os.system('sed -i "s/#LoadModule authn_dbd_module/LoadModule authn_dbd_module/" ' + HTTPD_CONF)
    os.system('sed -i "s/#LoadModule dbd_module/LoadModule dbd_module/" ' + HTTPD_CONF)
    os.system("service httpd restart")
    
    return _sucess(request)

def reauth(request, user):
    return _sucess(request)

def users(request):
    us = ["/users/{}/".format(dir) 
          for dir in os.listdir(settings.SVNROOT)
          if os.path.isdir(os.path.join(settings.SVNROOT, dir)) and not dir=='httpd'
          ]
    
    return render(request, 'list.html', {"list":us, "title":"Users"})

def projects(request, user):
    user_home = os.path.join(settings.SVNROOT,user)
    if not os.path.exists(user_home):
        messages.error(request, "User Not Found!")
        return render(request, 'ajax.json')
    else:
        
        projs = ["http://{}/svn/{}/{}/".format(settings.SVNHOST, user, dir) 
                for dir in os.listdir(user_home) if os.path.isdir(os.path.join(user_home, dir))
                ]
            
        return render(request, 'list.html', {"list":projs, "title":"Projects for " + user})

def rnew(request, user, msg=True):
    user_home = os.path.join(settings.SVNROOT,user)
    ret = _sucess
    
    if os.path.exists(user_home):
        if msg:
            messages.error(request, "User '{}' has been existed!".format(user))
            ret = _fail
    else:
        os.mkdir(user_home)
        _write_from_tpl('location.conf', 
                       Context({'root':settings.SVNROOT, 'user':user}), 
                       os.path.join(settings.SVNROOT, "httpd", user+".conf")
                       )
        with open(os.path.join(user_home, 'authz'), "w+") as f:
            f.write('[/]\n{user} = rw'.format(user = user))
            
        _chown(user_home, 'apache')
        os.system("service httpd reload")
        
        if msg:
            messages.info(request, 'User {} create sucess!'.format(user))
            
    return ret(request)

def rdel(request, user):
    user_home = os.path.join(settings.SVNROOT,user)
    ret = _sucess
    
    if not os.path.exists(user_home):
        messages.error(request, "User Not Found!")
        ret = _fail
    else:
        shutil.rmtree(user_home)
        os.remove(os.path.join(settings.SVNROOT, "httpd", user+".conf"))
        messages.info(request, "OK")
    
    return ret(request)

def pnew(request, user, proj):
    rnew(request, user, msg=False)
    
    proj_home = os.path.join(settings.SVNROOT,user, proj)
    ret = _sucess
    
    if os.path.exists(proj_home):
        messages.error(request, "Project '{}' has been existed!".format(proj))
        ret = _fail
    else:
        os.system("svnadmin create {}".format(proj_home))
        _chown(proj_home, 'apache')
        
        messages.info(request, "http://{}/svn/{}/{}/".format(settings.SVNHOST, user, proj))
    
    return ret(request)

def pdel(request, user, proj):
    proj_home = os.path.join(settings.SVNROOT,user, proj)
    ret = _sucess
    
    if not os.path.exists(proj_home):
        messages.error(request, "Project Not Found!")
        ret = _fail
    else:
        shutil.rmtree(proj_home)
        messages.info("OK")
    
    return ret(request)

def job(request):
    if request.GET.has_key('job') and request.GET.has_key('user'):
        job = request.GET['job']
        if request.GET.has_key('arg') and (job=='pnew' or job=='pdel'):
            return jobs[job](request, request.GET['user'], request.GET['arg'])
        elif job=='rnew' or job=='rdel' or job=='auth':
            return jobs[job](request, request.GET['user'])
    
    messages.error(request, "argument error!")
    return _sucess(request)

jobs = {"rnew":rnew, "pnew":pnew, "rdel":rdel, "pdel":pdel, 'auth':reauth}