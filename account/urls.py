from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.admin_login, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('index/', views.index, name="index"),
    path('templates/', views.template_list, name="template_list"),
    path('blogs/', views.blog_list, name="blog_list"),
]