from django.urls import path, include
from . import views

urlpatterns = [
    path('<slug>/', views.home, name="home"),
    path('<slug>/blogs/<page>/', views.blog_list, name="blog_list"),
]
