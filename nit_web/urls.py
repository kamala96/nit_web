from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from decouple import config
from django.conf.urls.static import static
from site_app import views

admin.site.site_header = f'NIT WEB ADMINISTRATION'
admin.site.site_title = f"NIT WEB ADMINISTRATION"
admin.site.index_title = 'Site Administration'

# To customize the error handling for 404 and 500 errors in Django
handler500 = views. custom_500_view
handler404 = views.catch_non_existing_paths

urlpatterns = [
    path(config('SECRET_ADMIN_URL') + '/admin/', admin.site.urls),
    path('', include('site_app.urls')),
]

# Only for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# Add the catch-all route at the end
urlpatterns += [
    re_path(r'^.*$', views.catch_non_existing_paths, name='catch_all'),
]
