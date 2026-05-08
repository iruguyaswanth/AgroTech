from django.urls import path
from . import views

app_name = 'farmers'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my-crops/', views.my_crops_view, name='my_crops'),
    path('add-crop/', views.add_crop_view, name='add_crop'),
    path('edit-crop/<int:crop_id>/', views.edit_crop_view, name='edit_crop'),
    path('delete-crop/<int:crop_id>/', views.delete_crop_view, name='delete_crop'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/update/<int:order_id>/', views.update_order_status_view, name='update_order'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('earnings/', views.earnings_view, name='earnings'),
]
