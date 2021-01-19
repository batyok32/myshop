from django import forms
from .models import Order
# from localflavor.us.forms import USZipCodeField
from django.utils.translation import gettext_lazy as _
# from crispy_forms.layout import Layout
# from crispy_forms.bootstrap import PrependedText

class OrderCreateForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['first_name', 'email', 'address', 'city', 'phone_number', 'order_notes']
        widgets = {
            'order_notes': forms.TextInput(attrs={'placeholder': _('Notes about your order, e.g. special notes for delivery.'),
                                                  'class': "form-control",
                                                   'aria-describedby': "basic-addon1"}),
            'phone_number': forms.TextInput(attrs={'placeholder': '61000000',}),
            }
        # helper.layout = Layout(PrependedText('phone_number', '+993'))
        