from django.urls import path, include
from django.conf import settings
import debug_toolbar

# Create here
urlpatterns = [
    path("", include("public.urls")),
]


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include("debug_toolbar.urls"))]