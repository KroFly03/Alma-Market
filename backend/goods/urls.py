from django.urls import path
from goods.views import ItemListView, ItemCreateView, ItemDetailView, ItemUpdateView, ItemDeleteView, \
    CharacteristicListView, GoodPDFView, CategoryListView, ManufacturerListView, SubCategoryListView

app_name = 'goods'

urlpatterns = [
    # Goods

    path('', ItemListView.as_view(), name='list_item'),
    path('/create', ItemCreateView.as_view(), name='create_item'),
    path('/<int:pk>', ItemDetailView.as_view(), name='detail_item'),
    path('/<int:pk>/update', ItemUpdateView.as_view(), name='update_item'),
    path('/<int:pk>/delete', ItemDeleteView.as_view(), name='delete_item'),

    # Characteristics

    path('/characteristics', CharacteristicListView.as_view(), name='list_characteristic'),

    # Categories

    path('/categories', CategoryListView.as_view(), name='list_category'),

    # Manufacturers

    path('/manufacturers', ManufacturerListView.as_view(), name='list_manufacturer'),

    # SubCategories

    path('/sub_categories', SubCategoryListView.as_view(), name='list_subcategory'),

    # PDF

    path('/pdf', GoodPDFView.as_view(), name='pdf_list_item')
]
