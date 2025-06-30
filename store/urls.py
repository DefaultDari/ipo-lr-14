from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'manufacturers', views.ManufacturerViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'cartitems', views.CartItemViewSet, basename='cartitem')
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
    path('checkout/', views.checkout, name='checkout'),
    path('api/', include(router.urls)),
]