from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("cms_content.urls", "cms_content"), namespace="cms_content")),
    path("", include(("pages.urls", "pages"), namespace="pages")),
]

handler500 = 'pages.views.custom_500_view'

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

