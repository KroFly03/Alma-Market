from django.urls import path

from orders.views import UserOrderListView
from users.views import UserBasketCreateView, UserBasketListView, UserBasketDestroyView, UserBasketUpdateView

urlpatterns = [
    path('/add', UserBasketCreateView.as_view()),
    path('', UserBasketListView.as_view()),
    path('/<int:item_id>/delete', UserBasketDestroyView.as_view()),
    path('/<int:item_id>/update', UserBasketUpdateView.as_view()),
    path('/user', UserOrderListView.as_view()),
]