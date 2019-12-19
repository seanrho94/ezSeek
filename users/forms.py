from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from RS.models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class JobSeekerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=False)
    name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea, required=False, max_length=500)
    location = forms.CharField(max_length=30, required=False)
    phone_no = forms.CharField(max_length=12, required=False)
    qualification = forms.CharField(max_length=30, required=False)
    profession = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phone_no', 'location', 'qualification', 'profession', 'bio', 'password1', 'password2',)

class CompanySignUpForm(UserCreationForm):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=254, required=False)
    industry = forms.CharField(required=False)
    location = forms.CharField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False, max_length=500)

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'industry', 'bio', 'location', 'password1', 'password2')

class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'industry','location', 'bio']

class JobseekerUpdateForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['name', 'phone_no', 'location', 'qualification', 'profession', 'bio']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']





