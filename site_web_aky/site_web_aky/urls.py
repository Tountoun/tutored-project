from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('aky/', include('application_web_aky.urls')),
    path( "accounts/" ,  include ( "django.contrib.auth.urls" )),
    path('', lambda request: redirect("aky/",permament=False))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
