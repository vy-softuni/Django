from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import ADMIN_SITE_NAME


admin.site.site_header = ADMIN_SITE_NAME
admin.site.site_title = ADMIN_SITE_NAME
admin.site.index_title = ADMIN_SITE_NAME


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
