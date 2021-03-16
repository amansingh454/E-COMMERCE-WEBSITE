from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/',views.contact,name='contact'),
    path('legal_notice/',views.legal_notice,name='legal_notice'),
    path('tac/',views.tac,name='tac'),
    path('faq',views.faq,name='faq'),
    path('sms/',views.sms,name='sms')

]