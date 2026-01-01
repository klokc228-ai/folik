from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/', views.checkout_view, name='place_order'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),

]
