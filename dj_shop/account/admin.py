from django.contrib import admin
from .models import Profile
from django.utils.safestring import mark_safe

# Вывод картинок в админке!
# def image_img(self):
#     if self.photo:
#         return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.photo.url))
#     else:
#         return '(Нет изображения)'
# image_img.short_description = 'Картинка'
# image_img.allow_tags = True

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'phone_number', 'updated']