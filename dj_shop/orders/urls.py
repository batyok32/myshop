from django.urls import path
from . import views
from account.views import order_detail

app_name = 'orders'

urlpatterns = [

    path('create/', views.order_create, name='order_create'),
    path('order/<int:id>/', order_detail, name='order'),
    path('admin/order/<int:order_id>/', views.admin_order_detail,
        name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/',
            views.admin_order_pdf,
            name='admin_order_pdf'),
]

