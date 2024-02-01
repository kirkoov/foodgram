from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

# from django.utils.translation import gettext_lazy as _


app_name = "foodgram"

urlpatterns = i18n_patterns(
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    # prefix_default_language=False
)

if settings.DEBUG:
    import debug_toolbar  # type: ignore[import-untyped]

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)


# When using Docker:
# (as per https://github.com/jazzband/django-debug-toolbar/blob/main/docs/
# installation.rst)
# if DEBUG:
#     import socket  # only if you haven't already imported this
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] +
# ["127.0.0.1", "10.0.2.2"]
