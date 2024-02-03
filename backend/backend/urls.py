from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# from django.utils.translation import gettext_lazy as _


app_name = "backend"

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    # prefix_default_language=False
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)


# When using Docker:
# (as per https://github.com/jazzband/django-debug-toolbar/blob/main/docs/
# installation.rst)
# if DEBUG:
#     import socket  # only if you haven't already imported this
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] +
# ["127.0.0.1", "10.0.2.2"]
