from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    CITIES = (
        ('Ag', 'Ashgabat'),
        ('Bl', 'Balkan'),
        ('Mr', 'Mary'),
        ('Dz', 'Dasoguz'),
        ('Lb', 'Lebap'),
    )
    first_name=models.CharField(_("name"), max_length=250)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address=models.CharField(_('address'), max_length=250)
    city = models.CharField(_('city'), choices=CITIES, max_length=2)
    phone_number = models.BigIntegerField(_('phone_number'), validators=[MinValueValidator(61000000),
                    MaxValueValidator(65999999)])
    updated=models.DateTimeField(auto_now=True)
    
    # class Meta:
    #     ordering = ['user.username']

    def __str__(self):
        return f'Profile for user {self.user.username}'
    