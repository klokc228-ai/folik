from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Product,
    CartItem,
    Order,
    OrderItem
)

# =====================
# ГЛАВНАЯ СТРАНИЦА
# =====================
def index(request):
    featured_products = Product.objects.filter(is_available=True).order_by('-featured_score','-is_featured','-created_at')[:6]
    return render(request, 'main/index.html', {
        'featured_products': featured_products
    })

# =====================
# СТРАНИЦА ТОВАРОВ
# =====================
def products(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'main/products.html', {
        'products': products
    })

# =====================
# ДЕТАЛИ ТОВАРА
# =====================
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main/product_detail.html', {
        'product': product
    })

# =====================
# КОРЗИНА
# =====================
def cart_view(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()

    cart_items = CartItem.objects.filter(session_key=session_key)
    cart_total = sum(item.get_total_price() for item in cart_items)

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()

    item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')

def remove_from_cart(request, item_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()

    item = get_object_or_404(
        CartItem,
        id=item_id,
        session_key=session_key
    )
    item.delete()
    return redirect('cart')

def update_quantity(request, item_id, action):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()

    item = get_object_or_404(
        CartItem,
        id=item_id,
        session_key=session_key
    )

    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect('cart')

# =====================
# ОФОРМЛЕНИЕ ЗАКАЗА
# =====================
def checkout_view(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()

    cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        return redirect('cart')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')

        if not full_name or not phone:
            return render(request, 'main/checkout.html', {
                'cart_items': cart_items,
                'error': 'Заполните все поля'
            })

        # 🔥 СОЗДАЁМ ЗАКАЗ (без пользователя)
        order = Order.objects.create(
            full_name=full_name,
            phone=phone
        )

        # 🔥 СОХРАНЯЕМ КАЖДЫЙ ТОВАР В ЗАКАЗ
        for item in cart_items:
            quantity = int(
                request.POST.get(
                    f'quantity_{item.id}',
                    item.quantity
                )
            )
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=quantity
            )

        # ❌ ОЧИЩАЕМ КОРЗИНУ
        cart_items.delete()

        return render(request, 'main/checkout.html', {
            'success': True,
            'cart_items': []
        })

    return render(request, 'main/checkout.html', {
        'cart_items': cart_items
    })

# =====================
# СТАТИЧЕСКИЕ СТРАНИЦЫ
# =====================
def about(request):
    return render(request, 'main/about.html')

def faq(request):
    return render(request, 'main/faq.html')
def buy_now(request, product_id):
    # Получаем товар
    product = get_object_or_404(Product, id=product_id)

    # Получаем session_key
    session_key = request.session.session_key
    if not session_key:
        request.session.create()

    # Добавляем товар в CartItem
    item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    # Редирект сразу на checkout
    return redirect('checkout')