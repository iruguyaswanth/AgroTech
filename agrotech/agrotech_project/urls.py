"""
AgroTech - Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile:
            if profile.role == 'farmer':
                return redirect('farmers:dashboard')
            elif profile.role == 'buyer':
                return redirect('buyers:home')
        if request.user.is_superuser:
            return redirect('admin_panel:dashboard')
    return redirect('accounts:login')

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('farmers/', include('farmers.urls', namespace='farmers')),
    path('buyers/', include('buyers.urls', namespace='buyers')),
    path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
