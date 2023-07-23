from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('api/goods', include('goods.urls')),
    path('api/orders', include('orders.urls')),
    path('api/auth', include('users.urls.auth')),
    path('api/users', include('users.urls.user')),
    path('api/basket', include('users.urls.basket')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
