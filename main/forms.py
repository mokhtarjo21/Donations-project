from django import forms
from users.models import User
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fname', 'lname', 'facebook_acount', 'Birthdate', 'phone', 'picture']
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control', }),
            'lname': forms.TextInput(attrs={'class': 'form-control', }),
            'facebook_acount': forms.URLInput(attrs={'class': 'form-control'}),
            'Birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }