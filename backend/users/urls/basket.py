from django.urls import path

from users.views import UserBasketCreateView, UserBasketListView, UserBasketDestroyView, UserBasketUpdateView

app_name = 'baskets'

urlpatterns = [
    path('/add', UserBasketCreateView.as_view(), name='add_basket_item'),
    path('', UserBasketListView.as_view(), name='list_basket_item'),
    path('/<int:item_id>/delete', UserBasketDestroyView.as_view(), name='delete_basket_item'),
    path('/<int:item_id>/update', UserBasketUpdateView.as_view(), name='update_basket_item'),
    # path('/user', UserOrderListView.as_view()),
]