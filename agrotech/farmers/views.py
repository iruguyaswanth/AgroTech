"""
Farmers Views
- Dashboard, Add/Edit/Delete Crop
- View and Update Orders
- View Reviews
- Earnings Table
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from farmers.models import Crop, Order, Review
from farmers.forms import CropForm, OrderStatusForm
from decimal import Decimal


def farmer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'farmer':
            messages.error(request, "This page is for farmers only.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@farmer_required
def dashboard_view(request):
    farmer = request.user
    crops = Crop.objects.filter(farmer=farmer)
    orders = Order.objects.filter(crop__farmer=farmer)

    total_crops = crops.count()
    active_crops = crops.filter(is_available=True).count()
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    delivered_orders = orders.filter(status='delivered').count()

    total_earnings = orders.filter(status='delivered').aggregate(
        total=Sum('total_price')
    )['total'] or Decimal('0.00')

    recent_orders = orders.order_by('-placed_on')[:5]

    context = {
        'total_crops': total_crops,
        'active_crops': active_crops,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'total_earnings': total_earnings,
        'recent_orders': recent_orders,
        'profile': farmer.profile,
    }
    return render(request, 'farmers/dashboard.html', context)


@farmer_required
def my_crops_view(request):
    crops = Crop.objects.filter(farmer=request.user).order_by('-created_on')
    return render(request, 'farmers/my_crops.html', {'crops': crops})


@farmer_required
def add_crop_view(request):
    form = CropForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        crop = form.save(commit=False)
        crop.farmer = request.user
        crop.save()
        messages.success(request, f"'{crop.name}' listed successfully!")
        return redirect('farmers:my_crops')
    return render(request, 'farmers/add_crop.html', {'form': form})


@farmer_required
def edit_crop_view(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer=request.user)
    form = CropForm(request.POST or None, request.FILES or None, instance=crop)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Crop updated successfully.")
        return redirect('farmers:my_crops')
    return render(request, 'farmers/edit_crop.html', {'form': form, 'crop': crop})


@farmer_required
def delete_crop_view(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, farmer=request.user)
    if request.method == 'POST':
        crop_name = crop.name
        crop.delete()
        messages.success(request, f"'{crop_name}' has been removed.")
        return redirect('farmers:my_crops')
    return render(request, 'farmers/delete_crop.html', {'crop': crop})


@farmer_required
def orders_view(request):
    status_filter = request.GET.get('status', '')
    orders = Order.objects.filter(crop__farmer=request.user).order_by('-placed_on')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'farmers/orders.html', {'orders': orders, 'status_filter': status_filter})


@farmer_required
def update_order_status_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, crop__farmer=request.user)
    form = OrderStatusForm(request.POST or None, instance=order)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"Order #{order.id} status updated to '{order.get_status_display()}'.")
        return redirect('farmers:orders')
    return render(request, 'farmers/update_order.html', {'form': form, 'order': order})


@farmer_required
def reviews_view(request):
    reviews = Review.objects.filter(crop__farmer=request.user).order_by('-created_on')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    if avg_rating:
        avg_rating = round(avg_rating, 1)
    return render(request, 'farmers/reviews.html', {'reviews': reviews, 'avg_rating': avg_rating})


@farmer_required
def earnings_view(request):
    orders = Order.objects.filter(crop__farmer=request.user, status='delivered').order_by('-placed_on')
    total = orders.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')

    # Earnings per crop
    crop_earnings = {}
    for order in orders:
        name = order.crop.name
        crop_earnings[name] = crop_earnings.get(name, Decimal('0.00')) + order.total_price

    return render(request, 'farmers/earnings.html', {
        'orders': orders,
        'total': total,
        'crop_earnings': crop_earnings,
    })
