from django import forms

from connector.models import RegisterModel

class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = RegisterModel
        fields = '__all__'
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput() 
        }
    


