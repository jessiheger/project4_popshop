from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Item, Category, Cart, Cart_items
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# import django decorator to post our form.
from django.views.decorators.http import require_http_methods
from .forms import CartAddItemForm, LoginForm

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

def cart_detail(request):
    if request.user.is_authenticated:
        print('USER is', request.user)
        cart = Cart.objects.get(user=request.user)
        items = Item.objects.filter(carts=cart).values()
        print("ITEMSSSS", items)
        for item in items:
            print('try to get CI')
            cart_item = Cart_items.objects.get(item=item['id'], cart=cart.id)
            print('CI', cart_item)
            print('QTY', cart_item.quantity)
            item['quantity'] = cart_item.quantity
            item['total_price'] = cart_item.quantity * item['price']
            item['update_quantity_form'] = CartAddItemForm(initial={'quantity': cart_item.quantity, 'update': True})
        return render(request, 'cart_detail.html', {'items': items})
    else:
        return redirect('index')

def cart_add(request, item_id):
    if request.user.is_authenticated:
        print('ADD ITEM SUCCESS', item_id) 
        cart = Cart.objects.get(user=request.user)
        item = Item.objects.get(id=item_id)
        new_cart_item = Cart_items()
        new_cart_item.cart = cart
        new_cart_item.item = item
        new_cart_item.quantity = 1
        new_cart_item.save()
        print('hit right before redirect on post request')
        return redirect('cart_detail')
    else:
        return redirect('index')

def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    # if item is removed, redirect user to cart_detail page (defined below)
    return redirect('cart_detail')


def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user. is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


# OLD CART_DETAIL VIEW:
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


