'''from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from .models import SellerProfile
User=get_user_model()
class UserRegistrationForm(forms.ModelForm):
    username=forms.CharField(label='username')
    email =forms.EmailField(label='emailaddress')
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model= User
        fields=[
            'username',
            'email',
            'password']

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get('username')
        email=self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username already exists')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        return super(UserRegistrationForm,self).clean(*args,**kwargs)'''


'''from django import forms
from django.contrib.auth.models import User
from .models import SellerProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

class UpdateSellerProfile(UserChangeForm):
    class Meta:
        model=SellerProfile
        fields = [
            'first_name',
            'last_name',
            'company_name',
            'company_location',
            'main_photo'
        ]

    def save(self, commit=True):
        user = super(UpdateSellerProfile, self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['lastname']
        user.company_name=self.cleaned_data['company_name']
        user.company_location=self.cleaned_data['company_location']
        if commit:
            user.save()
        return user'''