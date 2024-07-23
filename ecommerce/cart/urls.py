"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

app_name='cart'

urlpatterns = [
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('cart_views',views.cart_views,name='cart_views'),
    path('cart_remove/<int:id>',views.cart_remove,name='cart_remove'),
    path('cart_trash/<int:id>/<int:c_id>',views.cart_trash,name='cart_trash'),
    path('place_order/',views.place_order,name='place_order'),
    path('status/<u>',views.status,name='status'),
    path('your_orders',views.your_orders,name='your_orders'),
]