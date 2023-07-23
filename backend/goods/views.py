from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from goods.filters import ItemFilter
from goods.models import Item, Characteristic, Manufacturer, Category, SubCategory
from goods.serializers import SubCategorySerializer, CharacteristicSerializer, CategorySerializer, \
    ManufacturerSerializer, ItemSerializer, ItemCreateSerializer, ItemUpdateSerializer, ItemDeleteSerializer, \
    ItemPDFSerializer
from permissions import AdminRequired
from paginations import GoodPagination


class SubCategoryListView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    authentication_classes = []


class CharacteristicListView(generics.ListAPIView):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    authentication_classes = []


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    authentication_classes = []


class ManufacturerListView(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    authentication_classes = []


class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all().exclude(is_active=False)
    serializer_class = ItemSerializer
    pagination_class = GoodPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ItemFilter
    ordering = ['-id']
    search_fields = ['name']
    authentication_classes = []


class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = []


class ItemCreateView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemCreateSerializer
    permission_classes = [IsAuthenticated, AdminRequired]


class ItemUpdateView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemUpdateSerializer
    permission_classes = [IsAuthenticated, AdminRequired]
    http_method_names = ['patch']


class ItemDeleteView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDeleteSerializer
    permission_classes = [IsAuthenticated, AdminRequired]
    http_method_names = ['patch']


class GoodPDFView(generics.CreateAPIView):
    serializer_class = ItemPDFSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data, many=True)
        serializer.is_valid(raise_exception=True)
        return self.serializer_class.pdf(serializer, serializer.validated_data)
