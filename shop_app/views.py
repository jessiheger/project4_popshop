from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# import django decorator to post our form.
from django.views.decorators.http import require_http_methods
# from django.contrib.auth.forms import UserCreationForm
from .forms import CartAddItemForm, LoginForm, SignupForm
from .models import Item, Category, Cart, Cart_items

from django.views.generic.edit import UpdateView



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
        return redirect('login')

def add_to_cart(request, item_id):
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
        return redirect('login')

def delete_from_cart(request, item_id):
    if request.user.is_authenticated and request.method == "POST":
        cart = Cart.objects.get(user=request.user)
        print('user cart found', cart.id)
        item = Item.objects.get(id=item_id)
        print('item to be deleted is', item.name)
        # item_to_remove = Cart_items.objects.get(item=item_id)
        item_to_remove = Cart_items.objects.filter(id=item_id).delete()
        print("SAVED. Cart now looks like:", item_to_remove)
        cart.save()
        print('save worked')
        # item_to_remove.quantity = 0
        # item_to_remove.cart = cart 
        # item_to_remove.item = item
        # item_to_remove.save()
        # cart.save()
        print('hit right before redirect on delete request')
        return render(request, 'cart_detail.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            e = form.cleaned_data['email']
            p = form.cleaned_data['password']
            user = User.objects.create_user(username = u, email = e, password = p)
            print('created new user', user)
            user.save()
            print("saved new user:", user)
            user = authenticate(username = u, email = e, password = p)
            print("authenticated new user:", user)
            login(request,user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
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
    # return  HttpResponseRedirect('index')
    return redirect('index')



# def logout(request):
#     if request.user is not None:
#         if request.user. is_active:
#             logout(request)
#             return redirect('login')
#     else:
#         form = LoginForm()
#         return render(request, 'login.html', {'form': form})  


