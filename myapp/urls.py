from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    # path('api/post/', include('post.urls')),
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/schema/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
