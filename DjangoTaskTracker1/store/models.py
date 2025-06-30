from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal


class Category(models.Model):
    """Модель категории товара"""
    название = models.CharField(max_length=100, verbose_name="Название категории")
    описание = models.TextField(blank=True, null=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"
        
    def __str__(self):
        return self.название


class Manufacturer(models.Model):
    """Модель производителя"""
    название = models.CharField(max_length=100, verbose_name="Название производителя")
    страна = models.CharField(max_length=100, verbose_name="Страна")
    описание = models.TextField(blank=True, null=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        
    def __str__(self):
        return self.название


class Product(models.Model):
    """Модель товара"""
    название = models.CharField(max_length=200, verbose_name="Название товара")
    описание = models.TextField(verbose_name="Описание товара")
    фото_товара = models.ImageField(upload_to='products/', verbose_name="Фото товара", blank=True, null=True)
    цена = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    количество_на_складе = models.IntegerField(verbose_name="Количество на складе")
    категория = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    производитель = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    создан = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    обновлен = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-создан']
        
    def __str__(self):
        return self.название
    
    def clean(self):
        """Валидация модели"""
        if self.цена < 0:
            raise ValidationError({'цена': 'Цена не может быть отрицательной'})
        if self.количество_на_складе < 0:
            raise ValidationError({'количество_на_складе': 'Количество на складе не может быть отрицательным'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Модель корзины"""
    пользователь = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    дата_создания = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        
    def __str__(self):
        return f"Корзина пользователя {self.пользователь.username}"
    
    def общая_стоимость(self):
        """Вычисляет общую стоимость всех элементов корзины"""
        total = Decimal('0.00')
        for item in self.cartitem_set.all():
            total += item.стоимость_элемента()
        return total
    
    общая_стоимость.short_description = "Общая стоимость"


class CartItem(models.Model):
    """Модель элемента корзины"""
    корзина = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    товар = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    количество = models.PositiveIntegerField(verbose_name="Количество")
    добавлен = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ['корзина', 'товар']
        
    def __str__(self):
        return f"{self.товар.название} ({self.количество} шт.)"
    
    def стоимость_элемента(self):
        """Возвращает стоимость данного элемента корзины"""
        return self.товар.цена * self.количество
    
    стоимость_элемента.short_description = "Стоимость элемента"
    
    def clean(self):
        """Валидация модели"""
        if self.количество > self.товар.количество_на_складе:
            raise ValidationError({
                'количество': f'Количество не должно превышать доступное на складе ({self.товар.количество_на_складе} шт.)'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
