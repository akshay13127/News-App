# news/forms.py
from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, label='Search Keyword')
    from_date = forms.DateField(required=False, label='From Date')
    to_date = forms.DateField(required=False, label='To Date')
    source_name = forms.CharField(max_length=100, required=False, label='Source Name')
    category = forms.CharField(max_length=100, required=False, label='Category')
    language = forms.CharField(max_length=2, required=False, label='Language')


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')