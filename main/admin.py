from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem, CartItem


# --------------------
# ПРОДУКТЫ
# --------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" />'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = "Превью"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'is_available', 'is_featured', 'created_at', 'main_image_preview')
    list_filter = ('is_available', 'is_featured', 'created_at')
    search_fields = ('title',)
    inlines = [ProductImageInline]

    def main_image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" />'
        return "-"
    main_image_preview.allow_tags = True
    main_image_preview.short_description = "Главная фото"


# --------------------
# КОРЗИНА (без юзеров)
# --------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'get_user_display')

    def get_user_display(self, obj):
        # У тебя нет user в модели, используем session_key
        return obj.session_key if obj.session_key else "Аноним"
    get_user_display.short_description = "Пользователь"


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


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'get_total_price')

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Сумма'
