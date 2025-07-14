from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.conf import settings
import os



class Shopkeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    shop_description = models.TextField(blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    latitude = models.FloatField()
    longitude = models.FloatField()
    logo = models.ImageField(upload_to='shop_logos/', null=True, blank=True)
    shop_image = models.ImageField(upload_to='shop_images/', null=True, blank=True)
    business_hours = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    social_media = models.JSONField(default=dict, blank=True)
    categories = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.shop_name} ({self.user.username})"

class Product(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def stock_status(self):
        if self.stock == 0:
            return 'out_of_stock'
        elif self.stock <= 3:
            return 'low_stock'
        else:
            return 'in_stock'

    @property
    def is_available(self):
        return self.stock > 0

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='reviews')
    shop = models.ForeignKey('Shopkeeper', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['customer', 'shop']  # One review per shop per customer

    def __str__(self):
        return f"{self.customer.user.username}'s review for {self.shop.shop_name}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    profile_picture = models.ImageField(upload_to='customer_profiles/', null=True, blank=True)
    favorite_shops = models.ManyToManyField('Shopkeeper', related_name='favorited_by', blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    def save(self, *args, **kwargs):
        if not self.latitude:
            self.latitude = 0
        if not self.longitude:
            self.longitude = 0
        if self.profile_picture:
            # Get the file extension
            _, ext = os.path.splitext(self.profile_picture.name)
            # Set a unique filename
            self.profile_picture.name = f'customer_{self.user.username}{ext}'
        super().save(*args, **kwargs)

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('On Way', 'Customer On Way'),
        ('Arrived', 'Customer Arrived'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    customer_name = models.CharField(max_length=100)  # Keep this for backward compatibility
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    delivery_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_location_lat = models.FloatField(null=True, blank=True)
    last_location_lng = models.FloatField(null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    notification_sent = models.BooleanField(default=False)
    estimated_arrival = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} by {self.customer.user.username}"

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def save(self, *args, **kwargs):
        if not self.pk:  # New order being created
            # Update product stock
            if self.product.stock >= self.quantity:
                self.product.stock -= self.quantity
                self.product.save()
        super().save(*args, **kwargs)