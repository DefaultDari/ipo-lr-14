from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Manufacturer, Product, Cart, CartItem, Order, OrderItem

# 1. Сначала определим inline-классы
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['стоимость_элемента', 'добавлен']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['товар', 'количество', 'цена', 'сумма']

# 2. Регистрация моделей
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['название', 'описание']
    search_fields = ['название']
    list_filter = ['название']

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['название', 'страна']
    search_fields = ['название', 'страна']
    list_filter = ['страна']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['название', 'категория', 'производитель', 'цена', 'количество_на_складе', 'фото_preview']
    list_filter = ['категория', 'производитель', 'создан']
    search_fields = ['название', 'описание']
    list_editable = ['цена', 'количество_на_складе']
    readonly_fields = ['создан', 'обновлен', 'фото_preview']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('название', 'описание', 'фото_товара', 'фото_preview')
        }),
        ('Коммерческая информация', {
            'fields': ('цена', 'количество_на_складе', 'категория', 'производитель')
        }),
        ('Системная информация', {
            'fields': ('создан', 'обновлен'),
            'classes': ('collapse',)
        }),
    )
    
    def фото_preview(self, obj):
        if obj.фото_товара:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.фото_товара.url)
        return "Нет фото"
    фото_preview.short_description = "Превью фото"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['пользователь', 'дата_создания', 'общая_стоимость', 'количество_товаров']
    list_filter = ['дата_создания']
    search_fields = ['пользователь__username', 'пользователь__email']
    readonly_fields = ['дата_создания', 'общая_стоимость']
    inlines = [CartItemInline]
    
    def количество_товаров(self, obj):
        return obj.cartitem_set.count()
    количество_товаров.short_description = "Количество товаров"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['товар', 'корзина', 'количество', 'стоимость_элемента', 'добавлен']
    list_filter = ['добавлен', 'товар__категория']
    search_fields = ['товар__название', 'корзина__пользователь__username']
    readonly_fields = ['стоимость_элемента', 'добавлен']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'дата_создания', 'пользователь', 'общая_стоимость', 'items_count']
    list_filter = ['дата_создания']
    search_fields = ['id', 'пользователь__username', 'email']
    readonly_fields = ['дата_создания', 'общая_стоимость']
    inlines = [OrderItemInline]
    
    def items_count(self, obj):
        return obj.orderitem_set.count()
    items_count.short_description = "Товаров"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'заказ', 'товар', 'количество', 'цена', 'сумма']
    list_filter = ['заказ']
    search_fields = ['товар__название', 'заказ__id']

# Настройка админ-панели
admin.site.site_header = "Админ-панель Funtastik"
admin.site.site_title = "Funtastik Admin"
admin.site.index_title = "Управление магазином игрушек"