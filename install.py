
# *-* coding:utf-8 *-*
'''
Created on Aug 28, 2014

@author: leon
'''

from django.template import Context
from django.conf import settings
from svnauto.views import _write_from_tpl, _chown

import os

def install():
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
    _chown(ROOT, 'apache')
    os.system("service httpd restart")
    print "Complete!"