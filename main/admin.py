from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_available', 'is_featured', 'created_at')
    list_filter = ('is_available', 'is_featured', 'created_at')
    search_fields = ('title',)
    inlines = [ProductImageInline]


# --------------------
# ЗАКАЗЫ
# --------------------

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price')

    def total_price(self, obj):
        return obj.get_total_price()

    total_price.short_description = 'Сумма'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone',
        'user',
        'created_at',
        'is_processed',
        'order_total'
    )
    list_filter = ('is_processed', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]

    def order_total(self, obj):
        return sum(item.get_total_price() for item in obj.items.all())

    order_total.short_description = 'Итого'
