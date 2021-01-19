from decimal import Decimal 
from django.conf import settings
from shop.models import Product
# from django.core import serializers
from django.forms.models import model_to_dict
import copy
# import json


class Wishlist(object):

    def __init__(self, request):
        """
        Initialize the wishlist
        """
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.wishlist = wishlist

    def add(self, product_id):
        """
        Add a product  to the wishlist or update its quantity
        """
        product_id = str(product_id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = {}
        self.save()
    

    def save(self):
        # mark the session as 'modified' to make sure it gets saved
        self.session.modified=True

    
    def remove(self, product_id):
        """
        Remove a product from the wishlist
        """
        product_id = str(product_id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()


    def __iter__(self):
        """
        Iterate over the items  in the wishlist  and get the products from the database
        """
        product_ids = self.wishlist.keys()
        # get the product objects and add them to the wishlist
        products = Product.objects.filter(id__in=product_ids)
        # data = serializers.serialize("json", products)
        # print(data)
        # wishlist=copy.deep_copy(self.wishlist)
        wishlist=copy.deepcopy(self.wishlist)
        for product in products:
            product_id = product.id
            # data = model_to_dict( product )
            # product = json.dumps(data)
            print("Product and price", product, product.price)
            # product.price=str(product.price)
            wishlist[str(product_id)]['product']= product

        for item in wishlist.values():
            # item['price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        """
        Count all items in the wishlist
        """
        count=sum(1 for item in self.wishlist.keys())
        return count
        
    def clear(self):
        # remove WISHLIST from session
        del self.session[settings.WISHLIST_SESSION_ID]
        self.save()