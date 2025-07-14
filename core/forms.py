from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Shopkeeper, Product, Order, Customer, Review

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
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'placeholder': 'Enter your last name'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = Customer
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'rows': '3',
                'placeholder': 'Enter your address'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        customer = super().save(commit=False)
        if commit:
            # Save customer data
            customer.save()
            # Update user data
            user = customer.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
        return customer

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'rows': '4',
                'placeholder': 'Write your review here...'
            })
        }

class ShopkeeperProfileForm(forms.ModelForm):
    class Meta:
        model = Shopkeeper
        fields = ['shop_name', 'shop_description', 'address', 'phone', 
                 'logo', 'shop_image', 'business_hours', 'website', 
                 'categories', 'latitude', 'longitude']
        widgets = {
            'shop_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Enter your shop name'
            }),
            'shop_description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'rows': '3',
                'placeholder': 'Describe your shop'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'rows': '3',
                'placeholder': 'Enter your shop address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Enter your phone number'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'accept': 'image/*'
            }),
            'shop_image': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'accept': 'image/*'
            }),
            'business_hours': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'e.g., Mon-Fri: 9AM-6PM, Sat: 10AM-4PM'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'https://your-website.com'
            }),
            'categories': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'e.g., Electronics, Accessories, etc.'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'step': 'any'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-600',
                'step': 'any'
            })
        }