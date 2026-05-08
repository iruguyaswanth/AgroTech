from django.contrib import admin
from .models import Crop, Order, Review, Wishlist, Cart

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'category', 'price_per_kg', 'quantity_kg', 'is_available', 'created_on')
    list_filter = ('category', 'is_available', 'created_on')
    search_fields = ('name', 'farmer__email', 'farmer__username', 'location')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'crop', 'quantity_kg', 'total_price', 'status', 'placed_on')
    list_filter = ('status', 'placed_on', 'updated_on')
    search_fields = ('buyer__email', 'buyer__username', 'crop__name', 'phone')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'crop', 'rating', 'is_flagged', 'created_on')
    list_filter = ('rating', 'is_flagged', 'created_on')
    search_fields = ('buyer__email', 'buyer__username', 'crop__name')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'crop', 'added_on')
    list_filter = ('added_on',)
    search_fields = ('buyer__email', 'buyer__username', 'crop__name')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'crop', 'quantity_kg', 'added_on')
    list_filter = ('added_on',)
    search_fields = ('buyer__email', 'buyer__username', 'crop__name')
