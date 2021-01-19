from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .forms import CartAddProductForm
from .cart import Cart
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import json


def cart_add(request, product_id):
    cart = Cart(request)
    product=get_object_or_404(Product, id=product_id, amount__gte=1)
    if request.POST:
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if product.amount >= cd['quantity']:
                if cd['quantity'] >= 1:
                    cart.add(product=product,
                        quantity=cd['quantity'],
                        override_quantity=cd['override'])
                    return redirect('cart:cart_detail')
                else:
                    cart.remove(product=product)
                    if cart:
                        return redirect('cart:cart_detail')
                    return redirect('/')
            else:
                messages.error(request, _('We are really sorry but we dont have so much'))
                if cart:
                    return redirect('cart:cart_detail')
                else:
                    return redirect(product)
        else :
            messages.error(request, "Error")
            return redirect(request, 'cart:cart_detail', 
                          {'form': form})
    else:
        cart.add(product=product,
            quantity=1,
            override_quantity=False)
        return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if cart:
        return redirect('cart:cart_detail')
    return redirect('/')

def cart_detail(request):
    cart=Cart(request)
    # for item in cart:
    #     print('giving form to an item: ', item)
    #     item['update_quantity_form'] = CartAddProductForm(initial={
    #         'quantity': item['quantity'],
    #         'override': True})
    #     print('gived a form to an item: ', item['update_quantity_form'])
    #     cart.save()
    print('its my hope: ', cart)
    coupon_apply_form = CouponApplyForm()
    r=Recommender()
    if len(cart) >= 1:
        cart_products = [item['product'] for item in cart]
        recommended_products = r.suggest_products_for(cart_products,
                                                max_results=4) 

    else:
        recommended_products = None

    return render(request, 'cart/detail.html', 
                            {'cart':cart,
                            'coupon_apply_form': coupon_apply_form,
                            'recommended_products': recommended_products })