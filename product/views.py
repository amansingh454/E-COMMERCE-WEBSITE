from django.shortcuts import render
from .models import Product,Order
#from .forms import ProductForm
from Accounts.models import Registration
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse,reverse
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from .choices import CATEGORY_CHOICE,PRODUCT_COLOR,AVAILABILITY_CHOICE,COMPANY_NAME,RETURN_POLICY,PRICE_RANGE
from .models import Seller,Cart
from django.shortcuts import get_object_or_404
# Create your views here.
def product_detail(request,id):
    product=get_object_or_404(Product,id=id)
    category=product.category
    price_range=product.sale_price
    brand=product.brand
    suggested_product=Product.objects.all().filter(category=category,sale_price__lte=price_range,brand=brand)
    context={'product':product,
             'products':suggested_product}
    return render(request,'product/product_detail.html',context)
def products(request):
    cat_list=[]
    dic={}
    dic2={}
    dic3={}
    dic4={}
    l=0
    products=Product.objects.all().order_by('-id')
    print(products)
    for item in products:
        cat_list.append(item.category)
    cat_list=list(set(cat_list))
    print(cat_list)
    for item in cat_list:
        products_by_cat=Product.objects.all().filter(category=item)
        for product in products_by_cat:
            l+=1
            product=product.ProductName.upper()
            if product in dic4:
                dic4[product]+=1
            else:
                dic4[product]=1
        item=item.upper()
        dic[l]=dic4
        dic2[item]=dic
        dic={}
        l=0
        dic4={}

    print(dic2)
    #cart total bill


    latest_product=Product.objects.all().order_by('-id')
    items = Cart.objects.filter(user__id=request.user.id)
    sale_price = 0
    for i in items:
        sale_price += int(i.product.sale_price)
    #pagination
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    product_per_page = paginator.get_page(page)
    # filterd product
    if 'brand' in request.GET:
        brand=request.GET['brand']
        if brand:
            products=products.filter(brand__iexact=brand)
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            products=products.filter(category__iexact=category)
    if 'price_range' in request.GET:
        price_range = request.GET['price_range']
        if price_range:
            products=products.filter(price__lte=price_range)
    company_name = sorted(COMPANY_NAME.values())
    category_choices = sorted(CATEGORY_CHOICE.values())
    price_range= sorted(PRICE_RANGE.keys())
    context={'total_products':len(products),
             'products':products,
             'category':cat_list,
             'product_by_name':dic2,
             'latest_product':latest_product,
             'items':len(items),
             'products_per_page':product_per_page,
             'CATEGORY_CHOICE': category_choices,
             'COMPANY_NAME': company_name,
             'PRICE_RANGE': price_range,
             'sale_price':sale_price
             }
    return render(request,'product/products.html',context)
def compare(request):
    return render(request,'product/compare.html')
def add_products(request):
    context={}
    if request.method=='POST':
        product_name=request.POST['product_name']
        description=request.POST['description']
        category=request.POST['category']
        brand=request.POST['brand']
        price=request.POST['price']
        quantity=request.POST['quantity']
        color=request.POST['color']
        availability=request.POST['availability']
        return_policy=request.POST['return_policy']
        delivery_charge=request.POST['delivery_charge']
        publish_date=request.POST['publish_date']
        Discount_percent=request.POST['Discount_percent']
        offer_description = request.POST['offer_description']
        Terms_conditions = request.POST['Terms_conditions']

        main_photo=request.FILES['main_photo']
        user = User.objects.get(id=request.user.id)
        seller=Seller.objects.get(user__id=request.user.id)
        product=Product(seller=seller,ProductName=product_name,description=description,category=category,
                        return_policy=return_policy,delivery_charge=delivery_charge,stock=availability,
                        brand=brand,price=price,color=color,quantity=quantity,publish_date=publish_date,
                        Discount_percent=Discount_percent,offer_description=offer_description,
                        Terms_conditions=Terms_conditions,main_photo=main_photo)
        product.save()
        product.price = int(product.price)
        product.Discount_percent = int(product.Discount_percent)
        if product.Discount_percent == 0:
            product.sale_price = product.price
        else:
            product.sale_price = product.price - ((product.Discount_percent * product.price) // 100)
        product.save()
        if 'optional_photo1' in request.FILES:
            optional_photo1=request.FILES['optional_photo1']
            product.optional_photo1=optional_photo1

        if 'optional_photo2' in request.FILES:
            optional_photo2=request.FILES['optional_photo2']
            product.optional_photo2=optional_photo2

        if 'optional_photo3' in request.FILES:
            optional_photo3=request.FILES['optional_photo3']
            product.optional_photo3=optional_photo3

        product.save()
        messages.success(request,'product added successfully')
        return redirect('index')
    else:
        company_name=sorted(COMPANY_NAME.values())
        product_color=sorted(PRODUCT_COLOR.values())
        category_choices=sorted(CATEGORY_CHOICE.values())
        context={'CATEGORY_CHOICE':category_choices,
                 'COMPANY_NAME':company_name,
                 'RETURN_POLICY':RETURN_POLICY,
                 'AVAILABILITY_CHOICE':AVAILABILITY_CHOICE,
                 'PRODUCT_COLOR':product_color
                 }
        return render(request,'product/add_products.html',context)
def my_products(request):
    products=Product.objects.all().filter(seller__user__id=request.user.id)
    if 'brand' in request.GET:
        brand=request.GET['brand']
        if brand:
            products=products.filter(brand__iexact=brand)
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            products=products.filter(category__iexact=category)
    if 'price_range' in request.GET:
        price_range = request.GET['price_range']
        if price_range:
            products=products.filter(price__lte=price_range)
    company_name = sorted(COMPANY_NAME.values())
    category_choices = sorted(CATEGORY_CHOICE.values())
    price_range= sorted(PRICE_RANGE.keys())
    context={'total_products':len(products),
             'CATEGORY_CHOICE': category_choices,
             'COMPANY_NAME': company_name,
             'PRICE_RANGE': price_range,
             'products':products
             }
    return render(request,'product/my_products.html',context)

def products_by_category(request):
    return render(request,'product/product_by_category.html')
def sellers(request):
    sellers=Seller.objects.all()

    context={'sellers':sellers,
             'total_sellers':len(sellers)}
    return render(request,'product/sellers.html',context)

def special_offers(request):
    products=Product.objects.all()
    lis1=[]
    latest_product = Product.objects.all().order_by('-id')
    offer_products=Product.objects.all().order_by('-Discount_percent')
    for item in offer_products:
        if item.Discount_percent:
            lis1.append(item)

    if 'brand' in request.GET:
        brand=request.GET['brand']
        if brand:
            products=products.filter(brand__iexact=brand)
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            products=products.filter(category__iexact=category)
    if 'price_range' in request.GET:
        price_range = request.GET['price_range']
        if price_range:
            products=products.filter(price__lte=price_range)
    company_name = sorted(COMPANY_NAME.values())
    category_choices = sorted(CATEGORY_CHOICE.values())
    price_range= sorted(PRICE_RANGE.keys())
    context={'total_products':len(products),
             'CATEGORY_CHOICE': category_choices,
             'COMPANY_NAME': company_name,
             'PRICE_RANGE': price_range,
             'products':products,
             'latest_product':latest_product,
             'offer_product':lis1,
             'count':len(lis1)
             }
    return render(request,'offers/specialoffers.html',context)
def update_products(request,id):
    product=Product.objects.get(pk=id)
    if request.method=="POST":
        product_name = request.POST['product_name']
        description = request.POST['description']
        category = request.POST['category']
        brand = request.POST['brand']
        price = request.POST['price']
        quantity = request.POST['quantity']
        color = request.POST['color']
        availability = request.POST['availability']
        return_policy = request.POST['return_policy']
        delivery_charge = request.POST['delivery_charge']
        publish_date = request.POST['publish_date']
        Discount_percent=request.POST['Discount_percent']
        offer_description=request.POST['offer_description']
        Terms_conditions=request.POST['Terms_conditions']


        product.product_name=product_name
        product.description=description
        product.category=category
        product.brand=brand
        product.price=price
        product.quantity=quantity
        product.color=color
        product.availability=availability
        product.return_policy=return_policy
        product.delivery_charge=delivery_charge
        product.publish_date=publish_date
        product.Discount_percent=Discount_percent
        #converting string to int
        product.price=int(product.price)
        product.Discount_percent=int(product.Discount_percent)
        if product.Discount_percent==0:
            product.sale_price=product.price
        else:
            product.sale_price=product.price-((product.Discount_percent*product.price)//100)
        print(product.sale_price)
        product.Terms_conditions=Terms_conditions
        product.offer_description=offer_description
        if 'main_photo' in request.FILES:
            main_photo=request.FILES['main_photo']
            product.main_photo=main_photo

        if 'optional_photo1' in request.FILES:
            optional_photo1=request.FILES['optional_photo1']
            product.optional_photo1=optional_photo1

        if 'optional_photo2' in request.FILES:
            optional_photo2=request.FILES['optional_photo2']
            product.optional_photo2=optional_photo2

        if 'optional_photo3' in request.FILES:
            optional_photo3=request.FILES['optional_photo3']
            product.optional_photo3=optional_photo3
        product.save()
        messages.success(request,'product updated successfully')
        return redirect('my_products')
    company_name = sorted(COMPANY_NAME.values())
    product_color = sorted(PRODUCT_COLOR.values())
    category_choices = sorted(CATEGORY_CHOICE.values())
    context = {'CATEGORY_CHOICE': category_choices,
               'COMPANY_NAME': company_name,
               'RETURN_POLICY': RETURN_POLICY,
               'AVAILABILITY_CHOICE': AVAILABILITY_CHOICE,
               'PRODUCT_COLOR': product_color,
               'product':product
               }
    return render(request,'product/update_products.html',context)

def delete(request):
    context = {}
    if "pid" in request.GET:
        pid = request.GET["pid"]
        product = get_object_or_404(Product,id=pid)
        context["products"] = product
        if "action" in request.GET:
            product.delete()
            messages.success(request,'product deleted successfully')
            return redirect('my_products')
    return render(request,'product/delete.html',context)

def add_to_cart(request,id):
    product=Product.objects.get(pk=id)
    user=User.objects.get(id=request.user.id)
    if request.method=="POST":
        quantity=request.POST['quantity']

    if request.user.is_authenticated:
        if user.is_superuser:
            messages.error(request, 'Admin you are not allowed')
            return redirect('/')
        else:
            if request.method == "POST":
                quantity = request.POST['quantity']
                quantity=int(quantity)
                if quantity<product.quantity:
                    if Cart.objects.all().filter(product=product, user=user).exists():
                        cart = Cart.objects.get(product=product, user=user)
                        cart.quantity += quantity
                        cart.save()
                        messages.success(request, 'Product added to cart successfully')

                    else:
                        cart = Cart(product=product, user=user, quantity=quantity)
                        cart.save()
                        messages.success(request, 'Product added to cart successfully')
                    return HttpResponseRedirect('/')
                else:
                    messages.error(request,'items out of stock')
                    return HttpResponseRedirect('/')
            else:
                if Cart.objects.all().filter(product=product,user=user).exists():
                    cart=Cart.objects.get(product=product,user=user)
                    if cart.quantity<product.quantity:
                        cart.quantity+=1
                        cart.save()
                        messages.success(request, 'Already in cart!! updated quantity to cart ')
                    else:
                        messages.error(request,'items out of stock! Grab items of your cart soon')
                        return redirect('/')
                else:
                    cart=Cart(product=product,user=user,quantity=1)
                    cart.save()
                    messages.success(request,'Product added to cart successfully')
                return redirect('/')
    else:
        messages.error(request,'please login')
    return redirect('/')


def cart_details(request):
    items=Cart.objects.filter(user__id=request.user.id)
    sale_price,quantity,total,delivery=0,0,0,0

    for i in items:
        sale_price+=int(i.product.sale_price)*i.quantity
        quantity+=int(i.quantity)
        delivery+=int(i.product.delivery_charge)
        total+=int(i.product.price)*i.quantity
    context={'sale_price':sale_price,
             'quantity':quantity,
             'total':total,
             'delivery':delivery,
             }
    return JsonResponse(context)
def change_quantity(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(Cart, id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)

    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(Cart, id=id)
        cart_obj.delete()
        return HttpResponse(1)


def cart_data(request):
    items = Cart.objects.filter(user__id=request.user.id)
    context={'items':items}
    return render(request,'product/cart.html',context)

from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm

def process_payment(request):
    items=Cart.objects.all()
    product_name=""
    inv="INV10001-"
    amount=0
    prd_id=""
    cart_id=""

    for item in items:
        product_name+=str(item.product.ProductName)+"\n"
        inv+=str(item.id)+","
        amount+=int(item.product.sale_price)
        prd_id+=str(item.product.id)+","
        cart_id+=str(item.id)+","

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount':str(amount),
        'item_name':product_name,
        'invoice':inv,

        'notify_url': 'http://{}{}'.format('127.0.0.1:8000/',
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('payment_cancelled')),

    }
    user=User.objects.get(username=request.user.username)
    ord=Order(cust_id=user,cart_id=cart_id,prd_id=prd_id)
    ord.save()
    ord.inv_id=inv
    request.session["order_id"]=ord.id
    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'product/process_payment.html',{'form': form})
def payment_cancelled(request):
    return render(request,'product/payment_cancelled.html')
def payment_done(request):
    if 'order_id' in request.session:
        order_id=request.session['order_id']
        ord=get_object_or_404(Order,id=order_id)
        ord.status=True
        ord.save()
        for i in ord.cart_id.split(",")[:-1]:
            c=Cart.objects.get(id=i)
            c.status=True
            c.save()

    return render(request,'product/payment_done.html')
def order_history(request):
    all_prod=[]
    orders=Order.objects.filter(cust_id__id=request.user.id).order_by('-id')
    for order in orders:
        products=[]
        for id in order.prd_id.split(",")[:-1]:
            prd=Product.objects.get(id=id)
            products.append(prd)
        context={
            'products':products,
            'inv_id':order.inv_id,
            'order_date':order.order_date,
            'order_id':order.id,
            'status':order.status}

        all_prod.append(context)
    context1={'order_history':all_prod}
    return render(request,'product/order_history.html',context1)