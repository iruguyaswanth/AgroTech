"""
Farmers Models
- Crop: product listed by farmer
- Order: created by buyer
- Review: given by buyer to farmer
"""

from django.db import models
from accounts.models import User


class Crop(models.Model):
    CATEGORY_CHOICES = [
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains & Cereals'),
        ('pulses', 'Pulses & Legumes'),
        ('spices', 'Spices & Herbs'),
        ('dairy', 'Dairy Products'),
        ('other', 'Other'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='vegetables')
    description = models.TextField()
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_kg = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=150)
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.farmer.username}"

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def total_orders(self):
        return self.orders.count()


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='orders')
    quantity_kg = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_address = models.TextField()
    phone = models.CharField(max_length=15)
    note = models.TextField(blank=True)
    placed_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.crop.name}"

    def status_steps(self):
        all_steps = ['pending', 'confirmed', 'packed', 'shipped', 'delivered']
        current_index = all_steps.index(self.status) if self.status in all_steps else -1
        return [(step, i <= current_index) for i, step in enumerate(all_steps)]


class Review(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='reviews')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review', null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    is_flagged = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.buyer.username} on {self.crop.name}"


class Wishlist(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'crop')

    def __str__(self):
        return f"{self.buyer.username} wishlisted {self.crop.name}"


class Cart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='in_carts')
    quantity_kg = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('buyer', 'crop')

    def subtotal(self):
        return round(self.crop.price_per_kg * self.quantity_kg, 2)
