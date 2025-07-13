from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Shopkeeper, Product, Order, Customer

class ShopkeeperRegistrationForm(UserCreationForm):
    shop_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'placeholder': 'Enter your shop name'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'rows': '3',
            'placeholder': 'Enter your shop address'
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'placeholder': 'Enter your phone number'
        })
    )
    latitude = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'step': 'any'
        })
    )
    longitude = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'step': 'any'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].widget.attrs.update({
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600'
            })

    class Meta:
        model = UserCreationForm.Meta.model
        fields = ['username', 'password1', 'password2', 'shop_name', 'address', 'phone', 'latitude', 'longitude']

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [ 'phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'rows': '3',
                'placeholder': 'Enter your address'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600'
            })
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

class ShopkeeperProfileForm(forms.ModelForm):
    class Meta:
        model = Shopkeeper
        fields = ('shop_name', 'shop_description', 'address', 'phone', 
                 'logo', 'shop_image', 'business_hours', 'website', 
                 'categories', 'latitude', 'longitude')
        widgets = {
            'shop_description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded'}),
            'business_hours': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'website': forms.URLInput(attrs={'class': 'w-full p-2 border rounded'}),
            'categories': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

class CustomerRegistrationForm(UserCreationForm):
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'rows': '3'
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600'
        })
    )
    latitude = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'step': 'any'
        })
    )
    longitude = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'step': 'any'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].widget.attrs.update({
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600'
            })

    class Meta:
        model = UserCreationForm.Meta.model
        fields = ['username', 'password1', 'password2', 'address', 'phone', 'latitude', 'longitude']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'stock', 'image']

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class ShopkeeperProfileForm(forms.ModelForm):
    class Meta:
        model = Shopkeeper
        fields = ['shop_name', 'address', 'phone', 'latitude', 'longitude']