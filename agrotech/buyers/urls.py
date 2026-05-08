from django.urls import path
from . import views

app_name = 'buyers'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('crop/<int:crop_id>/', views.crop_detail_view, name='crop_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:crop_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('order/place/<int:crop_id>/', views.place_order_view, name='place_order'),
    path('orders/', views.my_orders_view, name='my_orders'),
    path('orders/track/<int:order_id>/', views.track_order_view, name='track_order'),
    path('orders/review/<int:order_id>/', views.give_review_view, name='give_review'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:crop_id>/', views.toggle_wishlist_view, name='toggle_wishlist'),
    path('refund-policy/', views.refund_policy_view, name='refund_policy'),
]
