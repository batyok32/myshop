from django import template
from ..models import Product
from django.shortcuts import get_object_or_404
from ..models import Category

register = template.Library()

@register.simple_tag
def total_products():
    return Product.objects.count()

@register.simple_tag
def total_products_list():
    product_list= Product.objects.all()
    return {'product_list':product_list}

@register.simple_tag
def total_category_list():
    category_list =Category.objects.all()
    return {'category_list':category_list}



@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})
