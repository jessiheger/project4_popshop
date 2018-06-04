from django.urls import path
from . import views

# appname = 'popshop'

urlpatterns = [
    path('', views.index, name='index'),
    path('<category_slug>/', views.index, name='by_category'),
    path('<item_slug>/', views.detail, name='detail'),
    path('user/<username>/', views.cart, name='cart'),
    path('add_item/', views.add_item, name='add_item'),
    path('delete_item/', views.delete_item, name='delete_item'),
    # path('change_quant/', views.change_quant, name='change_quant'),
]

#urls wish list:
# home page - list of items (GET)
# item detail (GET)
    # - add item to cart (POST)
# my cart (GET)
    # - delete item from cart (DELETE)
    # - change quantity (PUT)


### FROM CATCOLLECTR ###
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<int:cat_id>/', views.show, name='show'),
#     path('post_url/', views.post_cat, name='post_cat'),
#     path('user/<username>/', views.profile, name='profile'),
#     path('login/', views.login_view, name="login"),
#     path('logout/', views.logout_view, name="logout"),
#     path('like_cat/', views.like_cat, name='like_cat'),
# ]