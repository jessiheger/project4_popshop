from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Item, Category
# from .forms import CatForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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
def detail(request, id, slug):
    print('I FOUND THE DETAIL ROUTE', request) 
    item = get_object_or_404(item, id=id, slug=slug, available=True)
    context = {
        'item': item
    }
    return render(request, 'detail.html', context)


######### FIX THIS ONE ##############
#from detail view, allow user to add the item to their cart
def add_item(request):
    item_id = request.GET.get('item_id', None)
    quantity = 0
    if (item_id):
        item = Item.objects.get(id=int(item_id))
        if item is not None:
            quantity = item.quantity + 1
            item.quantity = quantity
            item.save()
    return HttpResponse(quantity)

# displays all items in user's cart
def cart(request, username):
    user = User.objects.get(username=username)
    items = Item.objects.filter(user=user)
    return render(request, 'cart.html', {'username': username, 'items': items})

######### FIX THIS ONE ##############
#from cart view, allow user to add the item to their cart
def delete_item(request):
    item_id = request.GET.get('item_id', None)
    if (item_id):
        item = Item.objects.get(id=int(item_id))
        if item is not None:
            quantity = item.quantity - 1
            item.quantity = quantity
            item.save()
    return HttpResponse(quantity)

