from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

githuburl="githubprofiles"



urlpatterns = patterns('',
    # Examples:
    url(r'^polls/$','polls.views.index'),
    url(r'^'+githuburl+'/$',githuburl+'.views.index'),
    url(r'^'+githuburl+'/showusers/$',githuburl+'.views.showusers'),
    url(r'^'+githuburl+'/userinfo/(?P<login>\w+)/$',githuburl+'.views.userinfo'),
    url(r'^'+githuburl+'/repos/(?P<login>\w+)/$',githuburl+'.views.repos'),
    url(r'^'+githuburl+'/repoinfo/(?P<name>\S+)/(?P<owner>\w+)/$',githuburl+'.views.repoinfo'),
                       
                       
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
