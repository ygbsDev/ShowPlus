from django import forms
from django.contrib.auth.models import User
from .models import *


class SignUpForms(forms.ModelForm):
	class Meta:
		model = SignUp
		fields = ['username', 'password', 'nickName', 'name', 'email', 'phone', 'CI', 'DI']
		
class LoginForms(forms.Form):
	class Meta:
		model = User
		fields = ['username', 'password']