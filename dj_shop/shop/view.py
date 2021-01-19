from django.conf import settings
from shop.models import Product
import redis

# connect to redis
redis_r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)



class View(object):

    def __init__(self, request):
        """
        Initialize view
        """
        self.session = request.session
        view = self.session.get(settings.SECOND_VIEW_SESSION_ID)
        if not view:
            # save an empty view in session
            view = self.session[settings.SECOND_VIEW_SESSION_ID] = {}
        self.view = view

    def add(self, product):
        """
        Add a product to view session 
        """
        product_id = str(product.id)

        if product_id not in self.view:
            redis_r.zincrby('product_ranking', 1, product.id)
            total_views = redis_r.incr(f'product:{product.id}:views')
            self.view[product_id]={'total_views':str(total_views)}
        else:
            total_views = redis_r.get(f'product:{product.id}:views')
        self.save()

    def save(self):
        self.session.modified=True

