from django.urls import path

from orders.views import UserOrderListView
from users.routers import CustomRouter
from users.views import CustomUserViewSet

app_name = 'users'

router = CustomRouter(trailing_slash=False)

router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [path('users/orders', UserOrderListView.as_view(), name='user_order_list')]

urlpatterns += router.urls
