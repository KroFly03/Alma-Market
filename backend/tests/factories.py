import factory.django
from pytest_factoryboy import register

from goods.models import Item, Characteristic, ItemCharacteristic, Category, Manufacturer, SubCategory
from orders.models import Address, Order, OrderGoods
from users.models import User, Basket


@register
class SubCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubCategory

    name = factory.Sequence(lambda n: f"SubCategory {n}")


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")

    @factory.post_generation
    def with_subcategories(self, create, extracted, **kwargs):
        if not create:
            return

        for _ in range(2):
            subcategory = SubCategoryFactory()
            self.subcategory.add(subcategory)


@register
class ManufacturerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manufacturer

    name = factory.Sequence(lambda n: f"Manufacturer {n}")


@register
class CharacteristicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Characteristic

    name = factory.Sequence(lambda n: f"Characteristic {n}")


@register
class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Sequence(lambda n: f"Item {n}")
    description = 'description'
    price = 1000
    amount = 5
    category = factory.SubFactory(CategoryFactory)
    manufacturer = factory.SubFactory(ManufacturerFactory)

    @factory.post_generation
    def with_characteristics(self, create, extracted, **kwargs):
        if not create:
            return

        for _ in range(2):
            characteristic = CharacteristicFactory()
            ItemCharacteristic.objects.create(item=self, characteristic=characteristic, value='value')


@register
class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    name = factory.Sequence(lambda n: f"Address {n}")
    longitude = 0.5
    latitude = 0.5


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"Email{n}@mail.ru")
    phone = factory.Sequence(lambda n: f"Phone {n}")
    role = 'user'
    is_active = True
    first_name = factory.Sequence(lambda n: f"First_name {n}")
    last_name = factory.Sequence(lambda n: f"Last_name {n}")

    @factory.post_generation
    def with_basket(self, create, extracted, **kwargs):
        if not create:
            return

        for _ in range(2):
            item = ItemFactory()
            Basket.objects.create(user=self, item=item, amount=1)


@register
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    address = factory.SubFactory(AddressFactory)

    @factory.post_generation
    def with_goods(self, create, extracted, **kwargs):
        if not create:
            return

        for _ in range(2):
            item = ItemFactory()
            OrderGoods.objects.create(order=self, item=item, amount=1)
