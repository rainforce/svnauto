from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('svnauto.views',
    # Examples:
    # url(r'^$', 'svnauto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#     url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'job'),
    url(r'^index\.php$', 'job'),
    url(r'^install/$', 'install'),
    url(r'^users/(?P<user>\w+)/(?P<proj>\w+)/new/$', 'pnew'),
    url(r'^users/(?P<user>\w+)/(?P<proj>\w+)/delete/$', 'pdel'),
    url(r'^users/(?P<user>\w+)/new/$', 'rnew'),
    url(r'^users/(?P<user>\w+)/delete/$', 'rdel'),
    url(r'^users/(?P<user>\w+)/auth/$', 'reauth'),
    url(r'^users/$', 'users'),
    url(r'^users/(?P<user>\w+)/$', 'projects'),
)
