# from django import forms

# # const variable = possible choices for # allowed to add to cart
# QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]

# class CartAddItemForm(forms.Form):
#     # Quantity field:
#     quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)
#     # Update field - either adds or updates number of item to the cart.
#     update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)