from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "id": "password1", }),
        label="Confirm Password",
    )


    class Meta:
        model = Account
        fields = ['fullname', 'email', 'phone_number', 'password', 'username']
        widgets = {
            'fullname': forms.TextInput(attrs={'placeholder': 'Full Name', 'id': 'fullname'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'id': 'username'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone', 'id': 'phone'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")

        if password and password1 and password != password1:
            self.add_error('password1', "Passwords do not match.")
        return cleaned_data
