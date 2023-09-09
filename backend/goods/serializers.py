import json

from django.db import IntegrityError, transaction
from rest_framework import serializers

from goods.models import ItemCharacteristic, Item, Characteristic, Category, Manufacturer, SubCategory


class ListWithTotalGoodsSerializer(serializers.ModelSerializer):
    total_goods = serializers.SerializerMethodField()

    def get_total_goods(self, obj):
        return obj.get_total_goods()


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'

    def create(self, validated_data):
        category_id = validated_data.pop('category', None)

        category = Category.objects.get(pk=category_id)

        if not category:
            raise serializers.ValidationError({'category': ['Данной категории не существует.']})

        sub_category = SubCategory.objects.create(**validated_data)

        category.subcategory.add(sub_category)

        category.save()

        return sub_category


class CategorySerializer(ListWithTotalGoodsSerializer):
    subcategory = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class ManufacturerSerializer(ListWithTotalGoodsSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'


class ItemCharacteristicSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='characteristic.id', read_only=True)
    name = serializers.CharField(source='characteristic.name')

    class Meta:
        model = ItemCharacteristic
        fields = ('id', 'name', 'value')


class ItemSerializer(serializers.ModelSerializer):
    characteristic = ItemCharacteristicSerializer(source='itemcharacteristic_set', many=True)
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    def to_representation(self, instance):
        if not instance.is_active and self.context['request'].method == 'GET' and 'id' in self.context['request'].path:
            raise serializers.ValidationError({'item': ['Данный товар помечен как неактивный.']})
        return super().to_representation(instance)

    class Meta:
        model = Item
        fields = '__all__'


class ItemBaseSerializer(serializers.ModelSerializer):
    characteristic = ItemCharacteristicSerializer(source='itemcharacteristic_set', many=True)

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('id', 'is_active',)

    def is_valid(self, *, raise_exception=False):
        image = self.initial_data.pop('image', [])
        self.initial_data = self.initial_data.pop('json', [])
        self.initial_data['image'] = json.dumps(image)
        print(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def save_characteristics(self, item, characteristics):
        try:
            for characteristic in characteristics:
                char_name = characteristic.get('characteristic', None).get('name', None)
                value = characteristic.get('value', None)

                char, _ = Characteristic.objects.get_or_create(name=char_name)

                ItemCharacteristic.objects.create(item=item, characteristic=char, value=value)
        except IntegrityError:
            raise serializers.ValidationError({"characteristics": ['Характеристики не должны повторяться.']})

    def save(self, **kwargs):
        with transaction.atomic():
            characteristics = self.validated_data.pop('itemcharacteristic_set', [])
            item = super().save(**kwargs)

            item.itemcharacteristic_set.all().delete()
            self.save_characteristics(item, characteristics)

            return item


class ItemCreateSerializer(ItemBaseSerializer):
    def create(self, validated_data):
        with transaction.atomic():
            try:
                characteristicss = validated_data.pop('itemcharacteristic_set', [])
                item = Item.objects.create(**validated_data)
                self.save_characteristics(item, characteristicss)
            except IntegrityError:
                raise serializers.ValidationError({"characteristics": ['Характеристики не должны повторяться.']})

        return item


class ItemUpdateSerializer(ItemBaseSerializer):
    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                characteristics = validated_data.pop('itemcharacteristic_set', [])
                item = super().update(instance, validated_data)

                instance.itemcharacteristic_set.all().delete()
                self.save_characteristics(item, characteristics)
            except IntegrityError:
                raise serializers.ValidationError({"characteristics": ['Характеристики не должны повторяться.']})

        return item


class ItemDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('is_active',)

    def update(self, instance, validated_data):
        if not instance.is_active:
            raise serializers.ValidationError({'item': ['Данный товар помечен как неактивный.']})

        instance.is_active = False
        instance.save()

        return instance
