from django.contrib import admin
from django.urls import path,include
#from Accounts.views import Login_View
#from .forms import UserLoginForm
from . import views
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    #path('login/',Login_View.as_view(template_name="Accounts/login.html",authentication_form=UserLoginForm),name="login")
    path('signup/',views.signup,name='signup'),
    path('check_user/',views.check_user,name="check_user"),
    path('logout/',views.logout,name='logout'),
    path('customerdashboard/',views.custdashboard,name='custdashboard'),
    path('sellerdashboard/',views.sellerdashboard,name='sellerdashboard'),
    path('adminprofile/',views.adminprofile,name='adminprofile'),
    path('changepass/',views.changepass,name='changepass'),
    path('customer_edit_profile/',views.customer_edit_profile,name="customer_edit_profile"),
    path('seller_edit_profile/',views.seller_edit_profile,name="seller_edit_profile"),
    # forgot password path

    path('reset_password/',auth_view.PasswordResetView.as_view(template_name='Accounts/password_reset.html'),name='reset_password'),
    path('reset_password_sent/',auth_view.PasswordResetDoneView.as_view(template_name='Accounts/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='Accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset_complete.html'),name='password_reset_complete'),
    #for third party verification

    path('accounts/', include('allauth.urls'))
]