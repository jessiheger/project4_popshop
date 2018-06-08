from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from .forms import CartAddItemForm, LoginForm, SignupForm
from .models import Item, Category, Cart, Cart_items
from django.urls import reverse


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
    print('ID of the Detail_View Item', item_id) 
    item = get_object_or_404(Item, id=item_id, available=True)
    #creates CartAddItemForm on each item detail view:
    cart_item_form = CartAddItemForm()
    context = {
        'item': item,
        'cart_item_form': cart_item_form
    }
    return render(request, 'detail.html', context)


###### CART FUNCTIONS ########
# See My Cart
@require_http_methods(["GET", "POST"])

def cart_detail(request):
    if request.user.is_authenticated:
        print('USER is', request.user)
        cart = Cart.objects.get(user=request.user)
        items = Item.objects.filter(carts=cart).values()
        # cart_items = Cart_items.objects.filter(item_id=item_id).values()
        print("ITEMS IN MY CART", items)
        cart_price = 0
        for item in items:
            cart_item = Cart_items.objects.get(item=item['id'], cart=cart.id)
            print('cart_item ID:', cart_item)
            print('QTY', cart_item.quantity)
            item['quantity'] = cart_item.quantity
            item['total_price'] = cart_item.quantity * item['price']
            cart_price += item['total_price']
            item['update_quantity_form'] = CartAddItemForm(initial={'quantity': cart_item.quantity, 'update': True})
        return render(request, 'cart_detail.html', {'items': items, 'cart_price': cart_price})
    else:
        return redirect('login')

##### TO DO: ADD IF ELSE STATEMENT (if new item, add one or input #; if existing item, change quantity)
# Add New Item to Cart or Change Quatity of Existing Cart Item
def add_to_cart(request, item_id):
    if request.user.is_authenticated:
        print('ID of item added to cart', item_id) 
        cart = Cart.objects.get(user=request.user)
        item = Item.objects.get(id=item_id)
        new_cart_item = Cart_items()
        new_cart_item.cart = cart
        new_cart_item.item = item
        quantity_change = request.POST['quantity']
        print('quantity change', quantity_change)
        # item_to_change = Cart_items.objects.get(item_id=item.id)
        # item_to_change.quantity = quantity_change
        # item_to_change.save(['quantity'])
        new_cart_item.quantity = quantity_change
        new_cart_item.save()
        return redirect('cart_detail')
    else:
        return redirect('login')

def update_quantity(request, item_id, cart_id):
    if request.user.is_authenticated:
        print('YAY UPDATE ROUTE')
        cart_item = Cart_items.objects.get(item=item_id, cart=cart_id)
        print('cart_item', cart_item)
        cart_item.quantity = request.POST['quantity']
        print('request.POST[quantity]', request.POST['quantity'])
        cart_item.save()
        return redirect('cart_detail')
    else:
        return redirect('login')


#Remove Item from Cart
def delete_from_cart(request, item_id):
    if request.user.is_authenticated and request.method == "POST":
        cart = Cart.objects.get(user=request.user)
        item = Item.objects.get(id=item_id)
        item_to_remove = Cart_items.objects.get(item_id=item_id)
        item_to_remove.delete() 
        items = Item.objects.filter(carts=cart).values()
        for item in items:
            cart_item = Cart_items.objects.get(item=item['id'], cart=cart.id)
            item['quantity'] = cart_item.quantity
            item['total_price'] = cart_item.quantity * item['price']
            item['update_quantity_form'] = CartAddItemForm(initial={'quantity': cart_item.quantity, 'update': True})
        return render(request, 'cart_detail.html', {'items': items})


###### AUTH FUNCTIONS ########
# Sign Up as new Customer
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

# Log in to site to create/view cart
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

# Log Out
def logout_view(request):
    logout(request)
    return redirect('index')

#### OTHER PAGE VIEWS ####
# See info about previously featured busineses
def previously_featured(request):
    print ("page is", request.path)
    return render(request, 'previously_featured.html') 

# About PopShop 
def about(request):
    print ("page is", request.path)
    return render(request, 'about.html') 


