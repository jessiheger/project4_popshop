from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Item, Category, Cart, Cart_items
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# import django decorator to post our form.
from django.views.decorators.http import require_http_methods
from .forms import CartAddItemForm

# Homepage - see all items
def index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    items = Item.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = Item.objects.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'items': items
    }
    return render(request, 'index.html', context)

# Shows detail of one item
def detail(request, item_id):
    print('I FOUND THE DETAIL ROUTE', item_id) 
    item = get_object_or_404(Item, id=item_id, available=True)
    #creates CartAddItemForm on each item detail view:
    cart_item_form = CartAddItemForm()
    context = {
        'item': item,
        'cart_item_form': cart_item_form
    }
    return render(request, 'detail.html', context)


###### CART FUNCTIONS ########

# Decorator to require that a view only accepts the POST method:
@require_http_methods(["GET", "POST"])

# def cart_detail(request):
#     print('HIHLSDHGKH')
#     if request.method == 'POST':
#         # cart = Cart(request)
#         for item in cart:
#             # uses the quantity property of the CartAddItemForm: 
#             item['update_quantity_form'] = CartAddItemForm(initial={'quantity': item['quantity'], 'update': True})
#         # render a template called cart_detail.html
#         return render(request, 'cart_detail.html', {'cart': cart})
#     else:
#         print('GET CART DETAIL?', Cart.items)
#         cart = Cart(user_id = request.user.id)
#         # cart= Cart(request)
#         return render(request, 'cart_detail.html')
#         return HttpResponse('STUB')


def cart_detail(request):
    print('USER is', request.user)
    cart = Cart.objects.all().filter(id=19)
    print('we hit the cart_detail request', cart)
    # for item in cart:
    #     item['update_quantity_form'] = CartAddItemForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart_detail.html', {'cart': cart})

def cart_add(request, item_id):
    print('ADD ITEM SUCCESS', item_id) 
    cart = Cart(request)
    # item = get_object_or_404(Item, id=item_id)
    form = CartAddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # cart.add(item=item, quantity=cd['quantity'], update_quantity=cd['update'])
        # cart_obj = form.save()
        added_item = Item.objects.get(id=item_id)
        # cart_obj.items.add(new_cart)
        print('is valid', added_item)
        # new_cart = Cart()
        # my_cart = Cart(items=added_item)
        # new_cart.save()
        new_cart = Cart.objects.create(items=added_item)
    print('hit right before redirect on post request')
    return redirect('cart_detail')

def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    # if item is removed, redirect user to cart_detail page (defined below)
    return redirect('cart_detail')

