from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CustomUser, AdminUser, MerchantUser, CustomerUser
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Extend your SignUpForm to include a profile picture
class ExtendedSignUpForm(UserCreationForm):
    # ... your existing fields ...
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'company_name', 'gst_details', 'address', 'profile_picture')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data.get('user_type')
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.is_active = False  # User will be activated after email confirmation
        user.save()
        # ... your existing user type conditions ...
        return user