# from django.shortcuts import render, redirect, get_object_or_404
# # import django decorator to post our form.
# from django.views.decorators.http import require_http_methods

# from shop_app.models import Item
# from .cart import Cart
# from .forms import CartAddItemForm

# # Decorator to require that a view only accepts the POST method:
# @require_http_methods(["POST"])
# # @require_http_methods(["GET"]) ------- Might need if I merge these views with the shop_app views

# def cart_add(request, item_id):
#     cart = Cart(request)
#     item = get_object_or_404(Item, id=item_id)
#     form = CartAddItemForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(item=item, quantity=cd['quantity'], update_quantity=cd['update'])
#     return redirect('cart:cart_detail')

# def cart_remove(request, item_id):
#     cart = Cart(request)
#     item = get_object_or_404(Item, id=item_id)
#     cart.remove(item)
#     # if item is removed, redirect user to cart_detail page (defined below)
#     return redirect('cart:cart_detail')


# def cart_detail(request):
#     cart = Cart(request)
#     for item in cart:
#         # uses the quantity property of the CartAddItemForm: 
#         item['update_quantity_form'] = CartAddItemForm(initial={'quantity': item['quantity'], 'update': True})
#     # render a template called detail.html
#     return render(request, 'cart_detail.html', {'cart': cart})