"""
Buyers Views
- Home (browse crops), Search, Crop Detail
- Cart, Place Order, Track Order
- Reviews, Wishlist
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from farmers.models import Crop, Order, Review, Cart, Wishlist
from buyers.forms import PlaceOrderForm, ReviewForm
from decimal import Decimal


def buyer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'buyer':
            messages.error(request, "This page is for buyers only.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def home_view(request):
    # Public page — all can browse
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '')

    crops = Crop.objects.filter(is_available=True).select_related('farmer')

    if query:
        crops = crops.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        crops = crops.filter(category=category)
    if location:
        crops = crops.filter(location__icontains=location)
    if min_price:
        crops = crops.filter(price_per_kg__gte=min_price)
    if max_price:
        crops = crops.filter(price_per_kg__lte=max_price)

    if sort == 'price_asc':
        crops = crops.order_by('price_per_kg')
    elif sort == 'price_desc':
        crops = crops.order_by('-price_per_kg')
    elif sort == 'newest':
        crops = crops.order_by('-created_on')
    else:
        crops = crops.order_by('-created_on')

    from farmers.models import Crop as CropModel
    categories = CropModel.CATEGORY_CHOICES

    context = {
        'crops': crops,
        'categories': categories,
        'query': query,
        'category': category,
        'location': location,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
    }
    return render(request, 'buyers/home.html', context)


def crop_detail_view(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, is_available=True)
    reviews = Review.objects.filter(crop=crop, is_flagged=False).order_by('-created_on')
    avg_rating = crop.average_rating()

    user_has_reviewed = False
    in_wishlist = False
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile and profile.role == 'buyer':
            user_has_reviewed = Review.objects.filter(crop=crop, buyer=request.user).exists()
            in_wishlist = Wishlist.objects.filter(crop=crop, buyer=request.user).exists()

    return render(request, 'buyers/crop_detail.html', {
        'crop': crop,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_has_reviewed': user_has_reviewed,
        'in_wishlist': in_wishlist,
    })


@buyer_required
def cart_view(request):
    cart_items = Cart.objects.filter(buyer=request.user).select_related('crop')
    grand_total = sum(item.subtotal() for item in cart_items)
    return render(request, 'buyers/cart.html', {'cart_items': cart_items, 'grand_total': grand_total})


@buyer_required
def add_to_cart_view(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, is_available=True)
    qty = Decimal(request.POST.get('quantity', '1'))

    cart_item, created = Cart.objects.get_or_create(buyer=request.user, crop=crop)
    if not created:
        cart_item.quantity_kg += qty
    else:
        cart_item.quantity_kg = qty
    cart_item.save()

    messages.success(request, f"'{crop.name}' added to cart.")
    return redirect('buyers:cart')


@buyer_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(Cart, id=item_id, buyer=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('buyers:cart')


@buyer_required
def place_order_view(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id, is_available=True)

    form = PlaceOrderForm(request.POST or None, initial={
        'phone': request.user.profile.phone,
        'delivery_address': request.user.profile.address,
    })

    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.buyer = request.user
        order.crop = crop
        order.total_price = crop.price_per_kg * order.quantity_kg
        order.save()
        Cart.objects.filter(buyer=request.user, crop=crop).delete()
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('buyers:my_orders')

    return render(request, 'buyers/place_order.html', {'form': form, 'crop': crop})


@buyer_required
def my_orders_view(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-placed_on')
    return render(request, 'buyers/my_orders.html', {'orders': orders})


@buyer_required
def track_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    steps = order.status_steps()
    has_review = hasattr(order, 'review')
    return render(request, 'buyers/track_order.html', {'order': order, 'steps': steps, 'has_review': has_review})


@buyer_required
def give_review_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)

    if order.status != 'delivered':
        messages.error(request, "You can only review after the order is delivered.")
        return redirect('buyers:track_order', order_id=order.id)

    if hasattr(order, 'review'):
        messages.info(request, "You already reviewed this order.")
        return redirect('buyers:track_order', order_id=order.id)

    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.buyer = request.user
        review.crop = order.crop
        review.order = order
        review.save()
        messages.success(request, "Thank you for your review!")
        return redirect('buyers:track_order', order_id=order.id)

    return render(request, 'buyers/give_review.html', {'form': form, 'order': order})


@buyer_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(buyer=request.user).select_related('crop')
    return render(request, 'buyers/wishlist.html', {'wishlist': wishlist})


@buyer_required
def toggle_wishlist_view(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    item, created = Wishlist.objects.get_or_create(buyer=request.user, crop=crop)
    if not created:
        item.delete()
        messages.info(request, f"'{crop.name}' removed from wishlist.")
    else:
        messages.success(request, f"'{crop.name}' added to wishlist.")
    return redirect('buyers:crop_detail', crop_id=crop.id)


def refund_policy_view(request):
    return render(request, 'buyers/refund_policy.html')
