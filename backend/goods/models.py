from django.db import models


class ModelWithName(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Characteristic(ModelWithName):
    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class Manufacturer(ModelWithName):
    def get_total_goods(self):
        return self.item_set.count()

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class SubCategory(ModelWithName):
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Category(ModelWithName):
    subcategory = models.ManyToManyField(SubCategory, verbose_name='Подкатегории')

    def get_total_goods(self):
        return self.item_set.count()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Item(ModelWithName):
    description = models.TextField(verbose_name='Описание', max_length=1000)
    price = models.PositiveIntegerField(verbose_name='Цена', )
    amount = models.PositiveSmallIntegerField(verbose_name='Количество', )
    image = models.ImageField(verbose_name='Изображение', upload_to='images/', default='images/default_image.png')
    characteristic = models.ManyToManyField(Characteristic, verbose_name='Характеристики', through='ItemCharacteristic')
    is_active = models.BooleanField(verbose_name='Статус', default=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ItemCharacteristic(models.Model):
    item = models.ForeignKey(Item, verbose_name='Товар', on_delete=models.CASCADE)
    characteristic = models.ForeignKey(Characteristic, verbose_name='Характеристика', on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товара'
        unique_together = ('item', 'characteristic')
