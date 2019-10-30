from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
#import views
from skrpt import views

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    url(r'^sktask/', include('sktask.urls')),
    url(r'^skconfig/', include('skconfig.urls')),
    url(r'^skaccounts/', include('skaccounts.urls')),
    url(r'^skyw/', include('skyw.urls')),
    url(r'^skrpt/', include('skrpt.urls')),
    url(r'^skworkorders/', include('skworkorders.urls')),
    url(r'^skrecord/', include('skrecord.urls')),
    url(r'^$',views.index,name="index"),
    url(r'^skcmdb/', include('skcmdb.urls')),

#     url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
