from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from environs import Env


env = Env()
env.read_env()

DEBUG = env.bool("DJANGO_DEBUG", default=False)


urlpatterns = [
    path(env("ADMIN_URL"), admin.site.urls),

    # Apps
    path('', include('pages.urls', namespace='pages')),
    path('accounts/', include('accounts.urls')),
    path('app', include('entries.urls', namespace='entries')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG == True:
    import debug_toolbar
    
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]