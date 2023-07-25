from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from paginations import UserPagination
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from users.models import Basket
from users.serializers import BasketSerializer, UserBasketUpdateSerializer, BasketCreateSerializer


class CustomUserViewSet(UserViewSet):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering = ['id']
    search_fields = ['first_name', 'last_name']
    pagination_class = UserPagination
    http_method_names = ['get', 'post', 'patch']
    default_permission_class = [IsAuthenticated]
    permissions = {
        'list': [IsAuthenticated, IsAdminUser],
        'create': [AllowAny]
    }

    def get_permissions(self):
        return [permissions() for permissions in self.permissions.get(self.action, self.default_permission_class)]


class UserBasketCreateView(CreateAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketCreateSerializer
    permission_classes = [IsAuthenticated]


class UserBasketListView(ListAPIView):
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Basket.objects.filter(user__pk=self.request.user.pk)


class UserBasketUpdateView(UpdateAPIView):
    serializer_class = UserBasketUpdateSerializer
    http_method_names = ['patch']
    lookup_field = 'item_id'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user.pk)


class UserBasketDestroyView(DestroyAPIView):
    lookup_field = 'item_id'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user.pk).all()
