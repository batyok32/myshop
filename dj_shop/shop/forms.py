from .models import Comment, Contact
from django import forms
from django.utils.translation import gettext_lazy as _

# OPTIONS=(
#     ("0", _("Default")),
#     ("1", _("Min price products")),
#     ("2", _("Max price products")),
#     ("3", _("Latest"))
#     )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
class SearchForm(forms.Form):
    query=forms.CharField(label=_('Search'), widget=forms.TextInput(attrs={'placeholder': _('What do yo u need?')}))

# not working
# class FilterForm(forms.Form):
#     # choices = forms.MultipleChoiceField(choices=OPTIONS)
#     choices = forms.ChoiceField(label='', choices=OPTIONS, widget=forms.Select())

# print FilterForm().as_p()

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Your name'),}),
            'phone_number': forms.TextInput(attrs={'placeholder': '61000000',}),
            'body': forms.TextInput(attrs={'placeholder': _('Your message'),}),
        }