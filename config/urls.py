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

    # User management
    path('accounts/', include('accounts.urls')),
    
    # Local Apps
    path('', include('pages.urls')),
    path('app/', include('entries.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG == True:
    import debug_toolbar
    
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]


admin.site.site_header = "Calliope Admin"
admin.site.site_title = "Calliope Admin Portal"
admin.site.index_title = "Calliope Admin Portal"