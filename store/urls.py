from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.product_list, name='product_list'),  # Изменено на catalog/
    path('catalog/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Добавлен product_id в URL
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),  # Добавлен item_id
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Добавлен item_id
    path('register/', views.register, name='register'),
    path('spec/', views.spec_list, name='spec_list'),
    path('spec/<int:pk>/', views.spec_detail, name='spec_detail'),
    
]