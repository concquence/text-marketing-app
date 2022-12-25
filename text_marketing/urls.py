from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from mass_texting.views import CustomerViewSet, CampaignViewSet, MessageViewSet
from rest_framework import routers
from .yasg import urlpatterns as swaggerurlpatterns

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'campaigns', CampaignViewSet)
router.register(r'messages', MessageViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.authtoken')),

]

urlpatterns += swaggerurlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
