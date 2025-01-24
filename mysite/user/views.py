from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import CustomUserCreationForm, FindUsernameForm, CustomPasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])  # 패스워드 설정
            user.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def user_profile(request):
    return render(request, 'user/profile.html')

def find_username(request):
    if request.method == 'POST':
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_mail(
                    'Your Username',
                    f'Your username is: {user.username}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                return render(request, 'user/find_username_done.html')
            except User.DoesNotExist:
                form.add_error('email', 'No user found with this email address.')
    else:
        form = FindUsernameForm()
    return render(request, 'user/find_username.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'user/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'


# Create your views here.
