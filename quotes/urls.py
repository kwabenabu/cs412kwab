from django.urls import path
from django.conf import settings
from . import views
urlpatterns = [
    # path(r'', views.home, name="home"),
     path(r'', views.main_page, name="main_page"),
     path(r'quotes', views.quotes_page, name="quotes_page"),
     path(r'show_all', views.show_all_page, name="show_all_page"),
     path(r'about', views.about_page, name="about_page")

]