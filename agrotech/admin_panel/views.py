"""
Admin Panel Views
- Dashboard overview
- KYC Approvals
- Manage Users (block/activate)
- Manage Reviews (flag/remove)
- View all Orders
- Dispute resolution notes
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count
from accounts.models import User, UserProfile
from farmers.models import Crop, Order, Review
from decimal import Decimal


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Admin access only.")
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard_view(request):
    total_users = User.objects.count()
    total_farmers = UserProfile.objects.filter(role='farmer').count()
    total_buyers = UserProfile.objects.filter(role='buyer').count()
    pending_kyc = UserProfile.objects.filter(kyc_status='pending').count()
    total_crops = Crop.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_price')
    )['total'] or Decimal('0.00')
    flagged_reviews = Review.objects.filter(is_flagged=True).count()

    recent_orders = Order.objects.select_related('buyer', 'crop').order_by('-placed_on')[:8]

    context = {
        'total_users': total_users,
        'total_farmers': total_farmers,
        'total_buyers': total_buyers,
        'pending_kyc': pending_kyc,
        'total_crops': total_crops,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'flagged_reviews': flagged_reviews,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def kyc_list_view(request):
    status_filter = request.GET.get('status', 'pending')
    kyc_profiles = UserProfile.objects.filter(kyc_status=status_filter).select_related('user').order_by('-kyc_submitted_on')
    return render(request, 'admin_panel/kyc_list.html', {
        'kyc_profiles': kyc_profiles,
        'status_filter': status_filter,
    })


@admin_required
def kyc_detail_view(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            profile.kyc_status = 'approved'
            profile.is_verified = True
            profile.kyc_reviewed_on = timezone.now()
            profile.save()
            messages.success(request, f"{profile.user.username}'s KYC approved.")
        elif action == 'reject':
            reason = request.POST.get('rejection_reason', '')
            profile.kyc_status = 'rejected'
            profile.is_verified = False
            profile.kyc_rejection_reason = reason
            profile.kyc_reviewed_on = timezone.now()
            profile.save()
            messages.warning(request, f"{profile.user.username}'s KYC rejected.")
        return redirect('admin_panel:kyc_list')
    return render(request, 'admin_panel/kyc_detail.html', {'profile': profile})


@admin_required
def users_list_view(request):
    role = request.GET.get('role', '')
    users = UserProfile.objects.select_related('user').order_by('-joined_on')
    if role:
        users = users.filter(role=role)
    return render(request, 'admin_panel/users_list.html', {'users': users, 'role': role})


@admin_required
def toggle_user_block_view(request, user_id):
    profile = get_object_or_404(UserProfile, user__id=user_id)
    profile.is_blocked = not profile.is_blocked
    profile.save()
    status = "blocked" if profile.is_blocked else "activated"
    messages.success(request, f"User {profile.user.username} has been {status}.")
    return redirect('admin_panel:users_list')


@admin_required
def reviews_list_view(request):
    show = request.GET.get('show', 'flagged')
    if show == 'all':
        reviews = Review.objects.select_related('buyer', 'crop').order_by('-created_on')
    else:
        reviews = Review.objects.filter(is_flagged=True).select_related('buyer', 'crop').order_by('-created_on')
    return render(request, 'admin_panel/reviews_list.html', {'reviews': reviews, 'show': show})


@admin_required
def delete_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Review deleted.")
    return redirect('admin_panel:reviews_list')


@admin_required
def unflag_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_flagged = False
    review.save()
    messages.info(request, "Review unflagged and kept.")
    return redirect('admin_panel:reviews_list')


@admin_required
def orders_list_view(request):
    status = request.GET.get('status', '')
    orders = Order.objects.select_related('buyer', 'crop', 'crop__farmer').order_by('-placed_on')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'admin_panel/orders_list.html', {'orders': orders, 'status': status})


@admin_required
def disputes_view(request):
    # Show cancelled orders as potential disputes
    disputes = Order.objects.filter(status='cancelled').select_related('buyer', 'crop', 'crop__farmer').order_by('-placed_on')
    return render(request, 'admin_panel/disputes.html', {'disputes': disputes})
