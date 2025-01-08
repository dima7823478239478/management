from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'second_name', 'age', 'adress', 'login', 'date_of_birth',
                  'email_adress', 'phone_number', 'is_active', 'is_staff', 'work_hours',
                  'amount_completed_offers', 'time_of_work']

class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control',
    }))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'second_name', 'age','is_active', 'is_staff', 'adress', 'date_of_birth', 'email_adress', 'phone_number', 'work_hours', 'amount_completed_offers', 'time_of_work']
