from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/',views.products,name="products"),

    path('compare/',views.compare,name='compare'),

    path('add_products/',views.add_products,name='add_products'),
    path('my_products/',views.my_products,name="my_products"),
    path('update/<int:id>/', views.update_products, name="update_products"),
    path('delete/',views.delete,name="delete"),
    path('details/<int:id>/',views.product_detail,name='product_detail'),
    path("product_by_category/",views.products_by_category,name="product_by_category"),
    #cart
    path('change_quantity/',views.change_quantity,name="change_quantity"),
    path('cart_data/',views.cart_data,name="cart_data"),

    path('sellers/',views.sellers,name="sellers"),

    path('special_offers/',views.special_offers,name='special_offers'),

    path('cart/<int:id>/',views.add_to_cart,name="add_to_cart"),
    path('cart_details/',views.cart_details,name="cart_details"),

    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process_payment/',views.process_payment,name="process_payment"),
    path('payment_done/', views.payment_done, name="payment_done"),
    path('payment_cancelled/', views.payment_cancelled, name="payment_cancelled"),
    path('order_history/',views.order_history,name="order_history")

]