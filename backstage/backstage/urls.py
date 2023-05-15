from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

"""
全局url分发 
"""

urlpatterns = [

    re_path('^(?P<version>[v1|v2]+)/api/', include(
        [
            path('user/', include('apps.account.urls')),
            path('spider/', include('apps.spider.urls'))
        ],
    )),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
