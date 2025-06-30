import os
import django
from django.utils import timezone
from decimal import Decimal
import sys

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'funtastik.settings')
try:
    django.setup()
except Exception as e:
    print(f"Ошибка при настройке Django: {e}")
    sys.exit(1)

from store.models import Category, Manufacturer, Product

def create_initial_data():
    try:
        # Создаем категории
        cat1 = Category.objects.create(название="Конструкторы", описание="Развивающие конструкторы для детей")
        cat2 = Category.objects.create(название="Куклы", описание="Куклы и аксессуары")
        
        # Создаем производителей
        man1 = Manufacturer.objects.create(название="LEGO", страна="Дания", описание="Мировой лидер в производстве конструкторов")
        man2 = Manufacturer.objects.create(название="Barbie", страна="США", описание="Производитель кукол Барби")
        
        # Создаем товары - используем Decimal для цены
        Product.objects.create(
            название="Конструктор LEGO City",
            описание="Большой набор для постройки города",
            цена=Decimal('2999.99'),
            количество_на_складе=10,
            категория=cat1,
            производитель=man1
        )
        
        Product.objects.create(
            название="Кукла Барби",
            описание="Классическая кукла Барби",
            цена=Decimal('1999.99'),
            количество_на_складе=15,
            категория=cat2,
            производитель=man2
        )
        
        print("Данные успешно созданы!")
        
    except Exception as e:
        print(f"Ошибка при создании данных: {e}")

if __name__ == "__main__":
    create_initial_data()