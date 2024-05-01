# Views for handling the forms
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ExtendedSignUpForm
from .models import CustomUser, AdminUser, MerchantUser, CustomerUser
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator

def register(request):
    if request.method == 'POST':
        form = ExtendedSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Email activation
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = ExtendedSignUpForm()
    return render(request, 'register.html', {'form': form})

def activation_sent_view(request):
    return render(request, 'activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not active and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('activation_complete')
    else:
        return render(request, 'activation_invalid.html')

# Don't forget to create the corresponding URL patterns and templates for these views.
