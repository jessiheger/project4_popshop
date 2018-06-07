from django.urls import path
from . import views
from django.conf.urls import url


# appname = 'popshop'

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('previously_featured/', views.previously_featured, name='previously_featured'),
    path('<category_slug>/', views.index, name='by_category'),
    path('<int:item_id>/detail/', views.detail, name='detail'),
    path('cart/append/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<item_id>/', views.delete_from_cart, name='delete_from_cart'),
]


#urls wish list:
# home page - list of items (GET)
# item detail (GET)
    # - add item to cart (POST)
# my cart (GET)
    # - delete item from cart (DELETE)
    # - change quantity (PUT)
