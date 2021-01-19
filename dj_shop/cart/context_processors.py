from .cart import Cart
from wishlist.wishlist import Wishlist
from shop.models import Category

def cart(request):
    return {'cart': Cart(request)}

def wishlist(request):
    return {'wishlist': Wishlist(request)}

def categories(request):
    return {'categories':Category.objects.all()}

