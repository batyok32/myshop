"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('wishlist', include('wishlist.urls', namespace='wishlist')),
    path('orders', include('orders.urls', namespace='orders')),
    path('coupons', include('coupons.urls', namespace='coupons')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    # path('__debug__/', include(debug_toolbar.urls)),
    path('', include('shop.urls', namespace='shop'))
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)
