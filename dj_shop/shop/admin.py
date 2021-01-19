from django.contrib import admin
from .models import Category, Product, Comment, Contact, Brand, Image
from django.utils.safestring import mark_safe
from parler.admin import TranslatableAdmin
from django.utils.translation import gettext_lazy as _

# Вывод картинок в админке!
def image_img(self):
    if self.image:
        return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" height="100" width="100"/></a>'.format(self.image.url))
    else:
        return _('(Нет изображения)')
image_img.short_description = _('Картинка')
image_img.allow_tags = True

# class ProductAdminForm(forms.ModelForm):
#     description = forms.CharField(widget=CKEditorUploadingWidget())

#     class Meta:
#         model = Product
#         fields = '__all__'
class ImageInline(admin.TabularInline):
    model = Image
    # raw_id_fields = ['product']
# class OrderItemInline(admin.TabularInline):
#     model=OrderItem
#     raw_id_fields=['product']

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', image_img,  'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = [ 'name', image_img, 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    inlines = [ImageInline]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'product', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'created')
    list_filter = ['created']
    search_fields = ('name', 'phone_number', 'body')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',image_img, 'slug')
    search_fields = ['name']
    prepopulated_fields = {'slug':('name',)}



