from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from product.models import Product,Cart
from math import ceil
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
# Create your views here.
def index(request):
    cat_list = []
    dic = {}
    dic2 = {}
    dic3 = {}
    dic4 = {}
    l = 0
    products = Product.objects.all()
    print(products)
    for item in products:
        cat_list.append(item.category)
    cat_list = list(set(cat_list))
    print(cat_list)
    for item in cat_list:
        products_by_cat = Product.objects.all().filter(category=item)
        for product in products_by_cat:
            l+=1
            product = product.ProductName.upper()
            if product in dic4:
                dic4[product] += 1
            else:
                dic4[product] = 1
        item = item.upper()
        dic[l] = dic4
        dic2[item] = dic
        dic = {}
        l = 0
        dic4 = {}


    latest_product=Product.objects.all().order_by('-id')
    items = Cart.objects.filter(user__id=request.user.id)
    sale_price = 0
    for i in items:
        sale_price += int(i.product.sale_price)
    context = {'total_products': len(products),
               'products': products,
               'category': cat_list,
               'product_by_name': dic2,
               'latest_product': latest_product,
               'items':len(items),
               'sale_price':sale_price
               }
    return render(request,'shop/index.html',context)
def about(request):
    cat_list = []
    dic = {}
    dic2 = {}
    dic3 = {}
    dic4 = {}
    l = 0
    products = Product.objects.all()
    print(products)
    for item in products:
        cat_list.append(item.category)
    cat_list = list(set(cat_list))
    print(cat_list)
    for item in cat_list:
        products_by_cat = Product.objects.all().filter(category=item)
        for product in products_by_cat:
            l += 1
            product = product.ProductName.upper()
            if product in dic4:
                dic4[product] += 1
            else:
                dic4[product] = 1
        item = item.upper()
        dic[l] = dic4
        dic2[item] = dic
        dic = {}
        l = 0
        dic4 = {}
    print(dic2)
    latest_product = Product.objects.all().order_by('-id')
    items = Cart.objects.filter(user__id=request.user.id)
    sale_price = 0
    for i in items:
        sale_price += int(i.product.sale_price)
    context = {'total_products': len(products),
               'products': products,
               'category': cat_list,
               'product_by_name': dic2,
               'latest_product': latest_product,
               'items':len(items),
               'sale_price':sale_price,}
    return render(request,'shop/about.html',context)
