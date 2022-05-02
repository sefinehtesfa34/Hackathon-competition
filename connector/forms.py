from django import forms

from connector.models import RegisterModel

class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = RegisterModel
        fields = '__all__'
    


