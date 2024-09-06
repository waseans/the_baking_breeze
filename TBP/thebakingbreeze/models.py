from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, help_text="Image of the product")
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Price of the product")
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, help_text="Rating of the product")
    material = models.CharField(max_length=255, blank=True, null=True, help_text="Material of the product, e.g., stainless steel")
    dimensions = models.CharField(max_length=255, blank=True, null=True, help_text="Dimensions of the product, e.g., 15 x 10 x 8 inches")
    weight = models.CharField(max_length=50, blank=True, null=True, help_text="Weight of the product, e.g., 5 lbs")
    color = models.CharField(max_length=50, blank=True, null=True, help_text="Color of the product, e.g., Silver")
    included_accessories = models.TextField(blank=True, null=True, help_text="List of included accessories, e.g., Baking tray, mixing bowl, whisk, spatula")

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('sent', 'Order Sent for Delivery'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')  # New field for status
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
