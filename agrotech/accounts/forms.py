"""
Accounts Forms
- Register, Login, KYC Upload, Profile Edit
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, UserProfile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))
    role = forms.ChoiceField(choices=[('farmer', 'Farmer'), ('buyer', 'Buyer')], widget=forms.RadioSelect)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data.get('phone', '')
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class KYCUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['kyc_document_type', 'kyc_document']
        widgets = {
            'kyc_document_type': forms.Select(choices=[
                ('', '-- Select Document Type --'),
                ('aadhaar', 'Aadhaar Card'),
                ('pan', 'PAN Card'),
                ('voter_id', 'Voter ID'),
                ('passport', 'Passport'),
                ('driving_license', 'Driving License'),
            ]),
        }
        labels = {
            'kyc_document_type': 'Document Type',
            'kyc_document': 'Upload Document Image',
        }


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_photo']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your address'}),
        }
