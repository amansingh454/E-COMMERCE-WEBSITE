from email.headerregistry import Group

from django.db import models
from datetime import datetime
from Accounts.models import User
from .choices import CATEGORY_CHOICE,PRODUCT_COLOR,AVAILABILITY_CHOICE,RETURN_POLICY,COMPANY_NAME
# Create your models here.

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mobile_number = models.CharField(max_length=10, default=None)
    address = models.TextField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, default='Noida', null=True)
    state = models.CharField(max_length=100, blank=True, default=None, null=True)
    postal_code = models.IntegerField(blank=True, default=None, null=True)
    age = models.IntegerField(default=20, null=True)
    gender = models.CharField(max_length=10, default='Male', null=True)
    country = models.CharField(max_length=50, blank=True, default=None, null=True)
    additional_information = models.TextField(max_length=100000, null=True, blank=True)
    image = models.ImageField(upload_to='Accounts', default=None, blank=True)
    shop_name=models.CharField(max_length=100,default=None,blank=True,null=True)
    shop_GST_no=models.CharField(max_length=100,default=None,blank=True,null=True)
    aadhar_card_no=models.CharField(max_length=100,default=None,blank=True,null=True)
    aadhar_pic=models.ImageField(upload_to='Accounts',default=None,blank=True,null=True)

    def __str__(self):
        return self.user.username
class Product(models.Model):
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE)
    ProductName=models.CharField(max_length=100,default=None)
    description = models.TextField(max_length=300000, default=None)
    category = models.CharField(max_length=100,default=None)
    brand=models.CharField(max_length=100,default=None)
    price=models.IntegerField(default=None,blank=True,null=True)
    quantity = models.IntegerField(default=None)
    stock=models.CharField(max_length=100,default=None,blank=True,null=True)
    color=models.CharField(max_length=100,default=None,blank=True)
    return_policy=models.CharField(max_length=100,default=None,blank=True)
    delivery_charge=models.IntegerField(default=0,blank=True,null=True)
    main_photo=models.ImageField(upload_to='products',blank=True)
    optional_photo1=models.ImageField(upload_to='products',blank=True)
    optional_photo2=models.ImageField(upload_to='products',blank=True)
    optional_photo3=models.ImageField(upload_to='products',blank=True)
    publish_date=models.DateTimeField(auto_now_add=False,auto_now=True)
    Discount_percent = models.IntegerField(default=0,blank=True,null=True)
    sale_price = models.IntegerField(default=0, blank=True, null=True)
    Terms_conditions = models.CharField(max_length=100000, default=None, blank=True,null=True)
    offer_description = models.TextField(max_length=100000, default=None,blank=True,null=True)

    class Meta:
        permissions=('edit_product','Can add product'),

    def __str__(self):
        return '{} by {}'.format(self.ProductName.upper(),self.seller.user.username.upper())

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    status=models.BooleanField(default=False)

    def __str__(self):
        return '{} by {}'.format(self.product.ProductName,self.user.username)
class Order(models.Model):
    cust_id=models.ForeignKey(User,on_delete=models.CASCADE)
    prd_id=models.CharField(max_length=100)
    cart_id=models.CharField(max_length=100)
    inv_id=models.CharField(max_length=100)
    status=models.BooleanField(default=False)
    order_date=models.DateTimeField(auto_now_add=False,auto_now=True)

    def __str__(self):
        return self.cust_id.username