from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, Order, OrderItem, CartItem

# Русские заголовки админки
admin.site.site_header = "Панель управления Folik"
admin.site.site_title = "Folik — Админка"
admin.site.index_title = "Управление сайтом"

# --------------------
# ПРОДУКТЫ
# --------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = "Превью"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'model_name', 'price', 'stock', 'is_available', 'is_featured', 'featured_score', 'created_at', 'main_image_preview')
    list_filter = ('is_available', 'is_featured', 'brand', 'condition', 'created_at')
    search_fields = ('title', 'brand', 'model_name', 'sku')
    list_editable = ('is_available', 'is_featured', 'featured_score')
    prepopulated_fields = { 'slug': ('title',) }
    inlines = [ProductImageInline]

    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image.url)
        return "-"
    main_image_preview.short_description = "Главная фото"


# --------------------
# КОРЗИНА (через сессии, без юзеров)
# --------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'get_user_display')

    def get_user_display(self, obj):
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
        # Безопасно считаем сумму, если product удалён
        return obj.get_total_price() if obj.product else 0
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
        # Суммируем только существующие продукты
        return sum(item.get_total_price() for item in obj.items.all() if item.product)
    order_total.short_description = 'Итого'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'get_total_price')

    def get_total_price(self, obj):
        # Безопасно, если продукт удалён
        return obj.get_total_price() if obj.product else 0
    get_total_price.short_description = 'Сумма'
