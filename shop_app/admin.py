
# Register your models here.
# from django.contrib import admin
# from .models import Category, Item

# admin.site.register([Category, Item])



from django.contrib import admin
from .models import Category, Item
 
 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
 
 
admin.site.register(Category, CategoryAdmin)
 
 
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available']
    list_filter = ['available']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
 
 
admin.site.register(Item, ItemAdmin)