from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .wishlist import Wishlist
from django.contrib import messages




def wishlist_add(request, product_id):
    wishlist = Wishlist(request)
    # product_id=int(product_id)
    product=get_object_or_404(Product, id=product_id)
    wishlist.add(product_id)
    print('added')
    return redirect('wishlist:wishlist_detail')
    


@require_POST
def wishlist_remove(request, product_id):
    wishlist = Wishlist(request)
    product=get_object_or_404(Product, id=product_id)
    wishlist.remove(product_id)
    return redirect('wishlist:wishlist_detail')

def wishlist_detail(request):
    wishlist=Wishlist(request)
    return render(request, 'wishlist/detail.html', {'wishlist':wishlist})