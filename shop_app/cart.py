# # import decimal data type to avoid issue of rounding off with regard to price.
# from decimal import Decimal
# from django.conf import settings
# from shop_app.models import Item

# ## Create class for Cart
# class Cart(object):
#     def __init__(self, request):
#         self.session = request.session
#         # cart = self.session.get(settings.CART_SESSION_ID)
#         cart = self.session
#         # if no cart in session, set an empty cart
#         if not cart:
#             cart = self.session = {}
#         self.cart = cart

#     #ADD ITEM TO CART
#     def add(self, item, quantity=1, update_quantity=False):
#         item_id = str(item.id)
#         if item_id not in self.cart:
#             self.cart[item_id] = {'quantity': 0, 'price': str(item.price)}
#             #price must be a string in order to serialize the session
#         if update_quantity:
#             self.cart[item_id]['quantity'] = quantity
#         else:
#             self.cart[item_id]['quantity'] += quantity
#         self.save()

#     #SAVES changes to cart in session
#     def save(self):
#         self.session = self.cart
#         self.session.modified = True

#     #REMOVES a single item from cart
#     def remove(self, item):
#         item_id = str(item.id)
#         if item_id in self.cart:
#             del self.cart[item_id]
#             self.save()

#     #iterate through the items in contained in the cart and get the related items.
#     def __iter__(self):
#         item_ids = self.cart.keys()
#         items = Item.objects.filter(id__in=item_ids)
#         for item in items:
#             self.cart[str(item.id)]['item'] = item

#         for item in self.cart.values():
#             item['price'] = Decimal(item['price'])
#             item['total_price'] = item['price'] * item['quantity']
#             yield item

#     #get total # of items in cart
#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())

#     #get sum of item $ values in cart
#     def get_total_price(self):
#         return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

#     #CLEAR the cart
#     def clear(self):
#         del self.session
#         self.session.modified = True