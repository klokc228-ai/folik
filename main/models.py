from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField



class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    image = CloudinaryField('image')  # 🔥 ВАЖНО

    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = CloudinaryField('image')  # 🔥 ВАЖНО

    def __str__(self):
        return f"Фото для {self.product.title}"

# ── КОРЗИНА (через сессии, без логина) ──
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    # сессия вместо пользователя
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def get_total_price(self):
        return (self.product.discount_price if self.product.discount_price else self.product.price) * self.quantity

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


# ── ЗАКАЗ ──
class Order(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ #{self.id} от {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return (self.product.discount_price if self.product.discount_price else self.product.price) * self.quantity

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"