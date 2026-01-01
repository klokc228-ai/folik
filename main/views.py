from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import (
    Product,
    CartItem,
    Order,
    OrderItem
)


def index(request):
    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    )
    return render(request, 'main/index.html', {
        'featured_products': featured_products
    })


def products(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'main/products.html', {
        'products': products
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'main/product_detail.html', {
        'product': product
    })


# =====================
# КОРЗИНА
# =====================

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.get_total_price() for item in cart_items)

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )
    item.delete()
    return redirect('cart')


@login_required
def update_quantity(request, item_id, action):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
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

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    # ❗ защита от пустой корзины
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

        # 🔥 СОЗДАЁМ ЗАКАЗ
        order = Order.objects.create(
            user=request.user,
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

        # ✅ СТРАНИЦА УСПЕХА
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
