from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('search/', views.product_search, name='product_search'),
    # path('search/<slug:filter_slug>/<slug:query>', views.product_search, name='product_search_filter'),
    path('filter/<slug:category_slug>/<slug:filter_slug>/', views.product_list,
         name='filter_products'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
        name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
        name='product_detail'),

]
