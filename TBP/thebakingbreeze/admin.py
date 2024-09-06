from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem

# Registering the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'material', 'dimensions', 'weight', 'color')
    search_fields = ('name', 'material', 'color')
    list_filter = ('rating', 'color', 'material')

# Registering the Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

# Registering the CartItem model
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product__name', 'cart__user__username')

# Registering the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status')
    search_fields = ('user__username', 'status')
    list_filter = ('status',)

# Registering the OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('product__name', 'order__user__username')
