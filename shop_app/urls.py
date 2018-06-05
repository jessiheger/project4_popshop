from django.urls import path
from . import views

# appname = 'popshop'

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('<category_slug>/', views.index, name='by_category'),
    path('<int:item_id>/detail/', views.detail, name='detail'),
    path('cart/append/<item_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<item_id>/', views.cart_remove, name='cart_remove'),
]

#urls wish list:
# home page - list of items (GET)
# item detail (GET)
    # - add item to cart (POST)
# my cart (GET)
    # - delete item from cart (DELETE)
    # - change quantity (PUT)
