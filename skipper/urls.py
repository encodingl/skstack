from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^skcmdb/', include('skcmdb.urls')),
#     url(r'^navi/', include('navi.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^sktask/', include('sktask.urls')),
    url(r'^skconfig/', include('skconfig.urls')),
    url(r'^skaccounts/', include('skaccounts.urls')),
    url(r'^skdomain/', include('skdomain.urls')),
    url(r'^skapi/', include('skapi.urls')),
#     url(r'^skdeploy/', include('skdeploy.urls')),
]