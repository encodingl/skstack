from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
#import views
from skrpt import views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'^skcmdb/', include('skcmdb.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^sktask/', include('sktask.urls')),
    url(r'^skconfig/', include('skconfig.urls')),
    url(r'^skaccounts/', include('skaccounts.urls')),
    url(r'^skdomain/', include('skdomain.urls')),
    url(r'^skyw/', include('skyw.urls')),
    url(r'^skapi/', include('skapi.urls')),
    url(r'^skrecord/', include('skrecord.urls')),
    url(r'^skrpt/', include('skrpt.urls')),
    url(r'^skdeploy/', include('skdeploy.urls')),
    url(r'^skworkorders/', include('skworkorders.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
