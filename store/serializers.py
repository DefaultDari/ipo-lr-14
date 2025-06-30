from rest_framework import serializers
from .models import Category, Manufacturer, Product, Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    категория = CategorySerializer(read_only=True)
    производитель = ManufacturerSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'фото_товара': {'required': False}
        }

class CartItemSerializer(serializers.ModelSerializer):
    товар = ProductSerializer(read_only=True)
    
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'пользователь', 'дата_создания', 'общая_стоимость', 'items']