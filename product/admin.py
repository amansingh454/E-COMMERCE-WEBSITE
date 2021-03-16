from django.contrib import admin
from .models import Product,Seller,Cart,Order
# Register your models here.
#from .models import Category
admin.site.register(Product)
#admin.site.register(Category)
admin.site.register(Seller)
admin.site.register(Cart)
admin.site.register(Order)
