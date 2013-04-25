from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'mock_project.myapp.views.list_posts'),
    url(r'^posts/(?P<post_slug>[^/]+)/$', 'mock_project.myapp.views.post'),
)
urlpatterns += staticfiles_urlpatterns()
