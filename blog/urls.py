from django.urls import path, include
from . import views

urlpatterns = [
    path('<slug:slug>/', views.home, name="home"),
    path('<slug:slug>/blogs/', views.blog_list, name="blog_list"),
]