from django.db import models
from django.urls import reverse
# Create your models here.
# from django.utils.safestring import mark_safe
from parler.models import TranslatableModel, TranslatedFields
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
import datetime
from decimal import Decimal 
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import floatformat
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Brand(models.Model):
    name=models.CharField(_("Name of brand"), max_length=100)
    slug = models.SlugField(_("slug"), unique=True)
    image=models.ImageField(upload_to='brands/')
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

class Category(TranslatableModel):

    translations = TranslatedFields(
        name = models.CharField(max_length=200,
                    db_index=True),
        slug = models.SlugField(max_length=200,
                    db_index=True,
                    unique=True)
    )
    image = models.ImageField(upload_to='category/')

    def __str__(self):
        return self.name

    
    class Meta:
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    # going to its unique url
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    # total category
    def get_total_category(self):
        total_category= Category.objects.count()
        return total_category
    



class Product(TranslatableModel):
    # Translated fields
    translations = TranslatedFields(
        name = models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True),
        description=RichTextUploadingField(blank=True)
    )

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand=models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    amount=models.IntegerField()
    discount=models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(100)])
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


    # going to its unique url
    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
    
    # total products
    def get_total_product(self):
        total_products= Product.objects.count()
        return total_products

    # to retrieve is this fresh product
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created <= now

    # retreive discount
    def get_discount(self):
        if self.discount:
            return (self.discount / Decimal(100)) * self.price
        return Decimal(0)

    # price after discount
    def get_price_after_dis(self):
        if self.discount:
            price = Decimal(self.price - self.get_discount())
            price = f'{price:.2f}'
            price = Decimal(price)
            return price
        # if product does not have discount
        else:
            return self.price

class Image(models.Model):
    product = models.ForeignKey(Product, related_name=_("images"), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
#     picture_desktop = ImageSpecField(
# source="picture",
# processors=[ResizeToFill(1200, 600)],
# format="JPEG",
# options={"quality": 100},
# )
# picture_tablet = ImageSpecField(
# source="picture", processors=[ResizeToFill(768, 384)],
# format="PNG"
# )
# picture_mobile = ImageSpecField(
# source="picture", processors=[ResizeToFill(640, 320)],
# format="PNG"
    # image_url = models.URLField(blank=True, null=True, unique=True, max_length=250)
    
    # def get_remote_image(self):
    #     if self.image_url:
    #         filename = urlparse(self.image_url).path.split('/')[-1]
    #         full_path = os.path.abspath('storeuno')
    #         try:
    #             result = urlretrieve(self.image_url, os.path.join(full_path + '/media/products/%Y/%m/%d', filename))
    #             self.original = '/media/products/%Y/%m/%d' + result[0].rsplit('/', 1)[-1]
    #             self.save()
    #         except urllib.error.HTTPError:
    #             pass

    # def __str__(self):
    #     return self.image_url[:10]

class Comment(models.Model):
    product = models.ForeignKey(Product,
            on_delete=models.CASCADE,
            related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True, null=True)
    body = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.product}'



class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    body = models.TextField()
    phone_number = models.IntegerField(validators=[MinValueValidator(61000000),
                    MaxValueValidator(65999999)])
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ('created',)
    
    def __str__(self):
        return f'Message by {self.name}'

