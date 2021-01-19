from django import forms
from django.utils.translation import gettext_lazy as _

# PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # quantity = forms.TypedChoiceField(
    #                 choices=PRODUCT_QUANTITY_CHOICES, 
    #                 coerce=int,
    #                 label=_(''))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "",}),)
    override = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput)
