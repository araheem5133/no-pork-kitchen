from django import forms

class registerForm(forms.Form):
    name = forms.CharField()
    address = forms.CharField()
    new_user = forms.CharField()
    