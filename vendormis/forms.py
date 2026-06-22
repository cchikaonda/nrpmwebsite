# vendormis/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PersonalDetail, DistrictOfOrigin, ResidentialAddress, BusinessDetail
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class VendorLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'id_password'
        })
    )

# -----------------------
# Step 1: User credentials
# -----------------------
class VendorRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# -----------------------
# Step 2: Personal details
# -----------------------
class PersonalDetailForm(forms.ModelForm):
    class Meta:
        model = PersonalDetail
        exclude = ['image']  # Optional: handle image separately
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'other_names': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Names'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}),
            'national_id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID Number'}),
        }


# -----------------------
# Step 3: District of Origin
# -----------------------
class DistrictOfOriginForm(forms.ModelForm):
    class Meta:
        model = DistrictOfOrigin
        exclude = ['personal_detail']
        widgets = {
            'district': forms.Select(attrs={'class': 'form-control'}),
            'traditional_authority': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.Select(attrs={'class': 'form-control'}),
        }


# -----------------------
# Step 4: Residential Address
# -----------------------
class ResidentialAddressForm(forms.ModelForm):
    class Meta:
        model = ResidentialAddress
        exclude = ['personal_detail']
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'traditional_authority': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.Select(attrs={'class': 'form-control'}),
        }


# -----------------------
# Step 5: Business Details
# -----------------------
class BusinessDetailForm(forms.ModelForm):
    class Meta:
        model = BusinessDetail
        exclude = ['personal_detail']
        widgets = {
            'sub_unit_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sub Unit Number'}),
            'shop_bench': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop / Bench'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}),
            'registration_certificate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration Certificate'}),
            'registration_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category_of_business': forms.Select(attrs={'class': 'form-control'}),
            'tpin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TPIN'}),
            'market': forms.Select(attrs={'class': 'form-control'}),
            'membership_of_association': forms.Select(attrs={'class': 'form-control'}),
            'date_joined': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
