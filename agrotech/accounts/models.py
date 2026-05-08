"""
Accounts Models
- Custom User (extends AbstractUser)
- UserProfile (role, kyc, verified badge)
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    ]

    KYC_STATUS = [
        ('not_submitted', 'Not Submitted'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    joined_on = models.DateTimeField(auto_now_add=True)

    # KYC
    kyc_document = models.ImageField(upload_to='kyc/', blank=True, null=True)
    kyc_document_type = models.CharField(max_length=30, blank=True)
    kyc_status = models.CharField(max_length=20, choices=KYC_STATUS, default='not_submitted')
    kyc_rejection_reason = models.TextField(blank=True)
    kyc_submitted_on = models.DateTimeField(blank=True, null=True)
    kyc_reviewed_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
