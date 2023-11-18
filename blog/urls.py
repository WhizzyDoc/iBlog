from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:title>/', views.home, name="home"),
    path('<str:title>/blogs/', views.blog_list, name="blog_list"),
]