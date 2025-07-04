# Generated by Django 5.1.6 on 2025-06-30 16:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_фото_товара'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('дата_создания', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('общая_стоимость', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общая стоимость')),
                ('адрес_доставки', models.TextField(verbose_name='Адрес доставки')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('телефон', models.CharField(max_length=20, verbose_name='Телефон')),
                ('пользователь', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-дата_создания'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('количество', models.PositiveIntegerField(verbose_name='Количество')),
                ('цена', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('заказ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order', verbose_name='Заказ')),
                ('товар', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Элемент заказа',
                'verbose_name_plural': 'Элементы заказа',
            },
        ),
    ]
