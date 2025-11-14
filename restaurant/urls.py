##restaurant/urls.py
# file urls.py
# author Kwabena Ampomah
# description Urls for the restaurant app
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.show_main, name='main'),
    path(r'order/', views.order_page, name='order_page'),
    path(r'confirmation/', views.confirmation, name='confirmation'),

]