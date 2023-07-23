from django.http import JsonResponse, Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from paginations import UserPagination
from djoser.views import UserViewSet
from users.filters import UserFilter
from users.models import Basket
from users.serializers import UserDeleteSerializer, UserBasketCreateSerializer, \
    UserBasketReadSerializer, UserBasketUpdateSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = None
    filterset_class = UserFilter
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        if self.action == 'list':
            self.pagination_class = UserPagination

        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UserDeleteSerializer

        return super().get_serializer_class()

    @swagger_auto_schema(
        operation_description="Returns list of users.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create user.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Returns user information.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Makes user unactive.")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(method='get', operation_description="Returns current user")
    @swagger_auto_schema(method='patch', operation_description="Edit current user profile.")
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)


class UserBasketCreateView(CreateAPIView):
    queryset = Basket.objects.all()
    serializer_class = UserBasketCreateSerializer

    @swagger_auto_schema(
        operation_description="Create new item in user basket.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_description="Returns list of user basket goods.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserBasketUpdateView(UpdateAPIView):
    serializer_class = UserBasketUpdateSerializer
    http_method_names = ['patch']
    lookup_field = 'item_id'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user.pk).all()

    @swagger_auto_schema(
        operation_description="Update amount of item in user basket.")
    def patch(self, request, *args, **kwargs):
        try:
            return super().patch(request, *args, **kwargs)
        except Http404:
            return JsonResponse({'item': 'Данный товар в корзине текущуего пользователя не найден'})


class UserBasketDestroyView(DestroyAPIView):
    lookup_field = 'item_id'

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user.pk).all()

    def get_object(self):
        return super().get_object()

    @swagger_auto_schema(
        operation_description="Delete item from user basket.")
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Http404:
            return JsonResponse({'item': 'Данный товар в корзине текущуего пользователя не найден'})
