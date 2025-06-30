from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Product, Category, Manufacturer, Cart, CartItem
import json
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from pathlib import Path

def load_specialties():
    # Load specialties from dump.json
    BASE_DIR = Path(__file__).resolve().parent.parent
    json_file = BASE_DIR / 'dump.json'
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    specialties = []
    for item in data:
        if item['model'] == 'data.specialty':
            specialties.append(item)
    
    return specialties

def spec_list(request):
    specialties = load_specialties()
    return render(request, 'store/spec_list.html', {
        'specialties': specialties,
        'title': 'Список квалификаций'
    })

def spec_detail(request, pk):
    specialties = load_specialties()
    spec = None
    
    for item in specialties:
        if item['pk'] == int(pk):
            spec = item
            break
    
    if not spec:
        raise Http404("Квалификация не найдена")
    
    return render(request, 'store/spec_detail.html', {
        'spec': spec,
        'title': spec['fields']['title']
    })
def index(request):
    """Главная страница"""
    featured_products = Product.objects.filter(количество_на_складе__gt=0)[:8]
    categories = Category.objects.all()
    return render(request, 'store/index.html', {
        'featured_products': featured_products,
        'categories': categories,
    })


def product_list(request):
    """Список товаров с фильтрацией"""
    products = Product.objects.filter(количество_на_складе__gt=0)
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()
    
    # Фильтрация
    category_id = request.GET.get('category')
    manufacturer_id = request.GET.get('manufacturer')
    search_query = request.GET.get('search')
    
    if category_id:
        products = products.filter(категория_id=category_id)
    
    if manufacturer_id:
        products = products.filter(производитель_id=manufacturer_id)
    
    if search_query:
        products = products.filter(
            Q(название__icontains=search_query) | 
            Q(описание__icontains=search_query)
        )
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'selected_category': int(category_id) if category_id else None,
        'selected_manufacturer': int(manufacturer_id) if manufacturer_id else None,
        'search_query': search_query,
    })


def product_detail(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        категория=product.категория,
        количество_на_складе__gt=0
    ).exclude(id=product.id)[:4]
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


@login_required
def cart_view(request):
    """Просмотр корзины"""
    cart, created = Cart.objects.get_or_create(пользователь=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
@require_POST
def add_to_cart(request):
    """Добавление товара в корзину"""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(пользователь=request.user)
    
    # Проверка наличия товара на складе
    if quantity > product.количество_на_складе:
        messages.error(request, f'Недостаточно товара на складе. Доступно: {product.количество_на_складе} шт.')
        return redirect('product_detail', product_id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        корзина=cart,
        товар=product,
        defaults={'количество': quantity}
    )
    
    if not created:
        # Проверка общего количества
        total_quantity = cart_item.количество + quantity
        if total_quantity > product.количество_на_складе:
            messages.error(request, f'Недостаточно товара на складе. Доступно: {product.количество_на_складе} шт.')
            return redirect('product_detail', product_id=product_id)
        
        cart_item.количество = total_quantity
        cart_item.save()
        messages.success(request, f'Количество товара "{product.название}" обновлено в корзине.')
    else:
        messages.success(request, f'Товар "{product.название}" добавлен в корзину.')
    
    return redirect('cart')


@login_required
@require_POST
def update_cart_item(request):
    """Обновление количества товара в корзине"""
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item = get_object_or_404(CartItem, id=item_id, корзина__пользователь=request.user)
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Товар удален из корзины.')
    elif quantity > cart_item.товар.количество_на_складе:
        messages.error(request, f'Недостаточно товара на складе. Доступно: {cart_item.товар.количество_на_складе} шт.')
    else:
        cart_item.количество = quantity
        cart_item.save()
        messages.success(request, 'Количество товара обновлено.')
    
    return redirect('cart')


@login_required
@require_POST
def remove_from_cart(request):
    """Удаление товара из корзины"""
    item_id = request.POST.get('item_id')
    cart_item = get_object_or_404(CartItem, id=item_id, корзина__пользователь=request.user)
    
    product_name = cart_item.товар.название
    cart_item.delete()
    messages.success(request, f'Товар "{product_name}" удален из корзины.')
    
    return redirect('cart')


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
