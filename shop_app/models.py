from django.db import models
from django.urls import reverse
# import decimal data type to avoid issue of rounding off with regard to price.
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)
 
    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'
 
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('by_category', args=[self.slug])
 
 
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='items/%Y/%m/%d', blank=True)
    carts = models.ManyToManyField('Cart', blank=False, through='Cart_items')
 
    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)
        # index_together meta option ^ specifies an index for id and slug fields. This will help improve performances of queries.
 
    def __str__(self):
        return self.name

## Create class for Cart
class Cart(models.Model):
    items = models.ManyToManyField('Item', blank=False, through='Cart_items')
    # items = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
        # ^ adds a reference to the User table in the db; if user is deleted, so is their cart
        
class Cart_items(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_items_join'








    # def __init__(self, request):
    #     self.session = request.session
    #     # cart = self.session.get(settings.CART_SESSION_ID)
    #     cart = self.session
    #     # if no cart in session, set an empty cart
    #     if not cart:
    #         cart = self.session = {}
    #     self.cart = cart

    # #ADD ITEM TO CART
    # def add(self, item, quantity=1, update_quantity=False):
    #     item_id = str(item.id)
    #     print('item_id', item_id)
    #     if item_id not in self.cart:
    #         self.cart[item_id] = {'quantity': 0, 'price': str(item.price)}
    #         #price must be a string in order to serialize the session
    #     if update_quantity:
    #         self.cart[item_id]['quantity'] = quantity
    #     else:
    #         self.cart[item_id]['quantity'] += quantity
    #     self.save()

    # # #SAVES changes to cart in session
    # def save(self):
    #     self.session = self.cart
    #     self.session.modified = True

    # #REMOVES a single item from cart
    # def remove(self, item):
    #     item_id = str(item.id)
    #     if item_id in self.cart:
    #         del self.cart[item_id]
    #         self.save()

    # # iterate through the items in contained in the cart and get the related items.
    # def __iter__(self):
    #     item_ids = self.cart.keys()
    #     items = Item.objects.filter(id__in=item_ids)
    #     for item in items:
    #         self.cart[str(item.id)]['item'] = item

    #     for item in self.cart.values():
    #         item['price'] = Decimal(item['price'])
    #         item['total_price'] = item['price'] * item['quantity']
    #         yield item

    # #get total # of items in cart
    # def __len__(self):
    #     return sum(item['quantity'] for item in self.cart.values())

    # #get sum of item $ values in cart
    # def get_total_price(self):
    #     return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # #CLEAR the cart
    # def clear(self):
    #     del self.session
    #     self.session.modified = True


#stretch goal - history of transactions

#store favorites?