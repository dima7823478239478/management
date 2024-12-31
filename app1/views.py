from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_data = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=login_data, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')  # Перенаправление после успешного входа
            else:
                form.add_error(None, 'Invalid login or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def main_view(request):
    return render(request, "main_manager.html")
