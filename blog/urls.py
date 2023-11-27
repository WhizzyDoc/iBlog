from django.urls import path, include
from . import views

urlpatterns = [
    path('<slug>/', views.home, name="home"),
    path('', views.home_page, name="home_page"),
    path('<slug>/blogs/<page>/', views.blog_list, name="blog_list"),
    path('<slug>/blogs/<type>/<type_slug>/<page>/', views.filter_blogs, name="filter_blogs"),
    path('<slug>/posts/<post_slug>/', views.blog_detail, name="blog_detail"),
    path('<slug>/contact/', views.contact, name="contact"),
    path('<slug>/about/', views.about, name="about"),
]
