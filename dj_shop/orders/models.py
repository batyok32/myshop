from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
# Create your models here.
from shop.models import Product
from django.conf import settings
from django.utils.translation import gettext as _
from django.urls import reverse
# from phonenumber_field.modelfields import PhoneNumberField

class Order(models.Model):
    CITIES = (
        ('Ag', 'Ashgabat'),
        ('Bl', 'Balkan'),
        ('Mr', 'Mary'),
        ('Dz', 'Dasoguz'),
        ('Lb', 'Lebap'),
    )
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(_("name"), max_length=50)
    # last_name=models.CharField(_(""), max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email =models.EmailField(_('email'), blank=True, null=True)
    address=models.CharField(_('address'), max_length=250)
    city = models.CharField(_('city'), choices=CITIES, max_length=2)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon,
            related_name='orders',
            null=True,
            blank=True,
            on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                validators=[MinValueValidator(0),
                    MaxValueValidator(100)])
    phone_number = models.BigIntegerField(_('phone_number'), validators=[MinValueValidator(61000000),
                    MaxValueValidator(65999999)])
    order_notes = models.TextField(_("order notes"))
    active=models.BooleanField(default='True')
    # phone_number=PhoneNumberField(null=True, blank=True)


    class Meta:
        ordering=['-created']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost=sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))
    
    def get_absolute_url(self):
        return reverse("orders:order", args=[self.id])
    
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product=models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
    