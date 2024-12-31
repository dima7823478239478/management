from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control',
    }))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))
