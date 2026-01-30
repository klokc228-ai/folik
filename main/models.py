from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField



class Product(models.Model):
    # Basic info
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=120, blank=True, null=True)
    model_name = models.CharField(max_length=120, blank=True, null=True)
    sku = models.CharField(max_length=80, blank=True, null=True, unique=False)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=False)

    # Technical specs (computer-themed)
    cpu = models.CharField(max_length=255, blank=True, null=True)
    ram_gb = models.PositiveIntegerField(default=0)
    storage_gb = models.PositiveIntegerField(default=0)
    storage_type = models.CharField(max_length=20, choices=(('SSD','SSD'),('HDD','HDD')), default='SSD')
    gpu = models.CharField(max_length=255, blank=True, null=True)
    operating_system = models.CharField(max_length=80, blank=True, null=True)
    condition = models.CharField(max_length=20, choices=(('new','New'),('used','Used'),('refurbished','Refurbished')), default='used')

    # Commerce
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    warranty_months = models.PositiveIntegerField(default=0)

    # Images / availability
    image = CloudinaryField('image', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)

    # Admin / ranking
    is_featured = models.BooleanField(default=False, help_text='Mark as featured (best products)')
    featured_score = models.FloatField(default=0.0, help_text='Higher means shown earlier in best products')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-featured_score', '-is_featured', '-created_at']

    def __str__(self):
        if self.brand and self.model_name:
            return f"{self.brand} {self.model_name}"
        return self.title

    def get_display_price(self):
        return self.discount_price if self.discount_price else self.price


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = CloudinaryField('image', blank=True, null=True)  # optional to allow admin create without Cloudinary configured

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