from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include
from django.views.decorators.cache import never_cache
from .routers import router

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    def mediafiles_urlpatterns(prefix):
        """
        Method for serve media files with runserver.
        """
        import re
        from django.views.static import serve

        return [
            re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve,
                {'document_root': settings.MEDIA_ROOT})
        ]

    # Hardcoded only for development server
    urlpatterns += staticfiles_urlpatterns(prefix="/static/")
    urlpatterns += mediafiles_urlpatterns(prefix="/media/")
