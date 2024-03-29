from django import forms

from .models import Order

class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'readonly': True})
        self.fields['last_name'].widget.attrs.update({'readonly': True})
        self.fields['email'].widget.attrs.update({'readonly': True})

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email']

