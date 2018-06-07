from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# const variable = possible choices for # allowed to add to cart
QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]

class CartAddItemForm(forms.Form):
    # Quantity field:
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int, widget=forms.Select(attrs={'name':'quantity'}))
    # Update field - either adds or updates number of item to the cart.
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

class SignupForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    email = forms.EmailField(max_length=200, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput())
