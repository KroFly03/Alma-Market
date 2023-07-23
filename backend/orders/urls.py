from django.urls import path

from orders.views import OrderListView, OrderCreateView, OrderDetailView, OrderUpdateView, OrderDeleteView, \
    AddressListView

app_name = 'orders'

urlpatterns = [
    # Orders

    path('', OrderListView.as_view(), name='list_order'),
    path('/create', OrderCreateView.as_view(), name='create_order'),
    path('/<int:pk>', OrderDetailView.as_view(), name='detail_order'),
    path('/<int:pk>/update', OrderUpdateView.as_view(), name='update_order'),
    path('/<int:pk>/delete', OrderDeleteView.as_view(), name='delete_order'),

    # Address

    path('/address', AddressListView.as_view(), name='list_address'),
]