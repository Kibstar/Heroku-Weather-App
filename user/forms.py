from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm): ## Custom User creation form
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=50, required=True)


    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2'] ## These values are references to built in arguments

# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(max_length=50, required=True)
#     last_name = forms.CharField(max_length=50, required=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email',]
#
# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image','bio']