from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from paginations import UserPagination
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from permissions import AdminRequired
from users.models import Basket
from users.serializers import UserDeleteSerializer, UserBasketCreateSerializer, \
    UserBasketReadSerializer, UserBasketUpdateSerializer


class CustomUserViewSet(UserViewSet):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering = ['id']
    search_fields = ['first_name', 'last_name']
    pagination_class = UserPagination
    http_method_names = ['get', 'post', 'patch']
    default_permission_class = [IsAuthenticated]
    permissions = {
        'list': [IsAuthenticated, IsAdminUser],
    }

    def get_permissions(self):
        return [permissions() for permissions in self.permissions.get(self.action, self.default_permission_class)]

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UserDeleteSerializer

        return super().get_serializer_class()


class UserBasketCreateView(CreateAPIView):
    queryset = Basket.objects.all()
    serializer_class = UserBasketCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class UserBasketListView(ListAPIView):
    serializer_class = UserBasketReadSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Basket.objects.all()

        user = self.request.user.pk

        if user:
            queryset = queryset.filter(user__pk=user).order_by('id')
        else:
            queryset = None

        return queryset


class UserBasketUpdateView(UpdateAPIView):
    serializer_class = UserBasketUpdateSerializer
    http_method_names = ['patch']
    lookup_field = 'item_id'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user.pk).all()


class UserBasketDestroyView(DestroyAPIView):
    lookup_field = 'item_id'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user.pk).all()

    def get_object(self):
        return super().get_object()
