from django.contrib import admin
from .models import Shopkeeper, Product, Order, Customer

@admin.register(Shopkeeper)
class ShopkeeperAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'phone', 'latitude', 'longitude')
    search_fields = ('shop_name', 'user__username')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shopkeeper', 'price', 'stock')
    list_filter = ('shopkeeper',)
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'latitude', 'longitude')
    search_fields = ('user__username', 'phone')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__user__username', 'product__name')