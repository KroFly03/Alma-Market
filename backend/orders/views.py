from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from paginations import OrderPagination
from orders.models import Order, Address
from orders.serializers import OrderSerializer, AddressReadSerializer, OrderCreateSerializer, \
    OrderDeleteSerializer, OrderUpdateSerializer


class AddressListView(ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressReadSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    permission_classes = []


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering = ['-created']
    search_fields = ['code']


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]


class OrderUpdateView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ['patch']


class OrderDeleteView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDeleteSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ['patch']


class UserOrderListView(OrderListView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user__pk=self.request.user)
