from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('kyc/', views.kyc_list_view, name='kyc_list'),
    path('kyc/<int:profile_id>/', views.kyc_detail_view, name='kyc_detail'),
    path('users/', views.users_list_view, name='users_list'),
    path('users/toggle-block/<int:user_id>/', views.toggle_user_block_view, name='toggle_block'),
    path('reviews/', views.reviews_list_view, name='reviews_list'),
    path('reviews/delete/<int:review_id>/', views.delete_review_view, name='delete_review'),
    path('reviews/unflag/<int:review_id>/', views.unflag_review_view, name='unflag_review'),
    path('orders/', views.orders_list_view, name='orders_list'),
    path('disputes/', views.disputes_view, name='disputes'),
]
