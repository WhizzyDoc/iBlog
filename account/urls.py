from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.admin_login, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('index/', views.index, name="index"),
    path('site/create/', views.create_site, name="create_site"),
    path('site/edit/', views.edit_site, name="edit_site"),
    path('templates/', views.template_list, name="template_list"),
    path('blogs/', views.blog_list, name="blog_list"),
    path('blogs/add/', views.add_blog, name="add_blog"),
    path('blogs/<id>/edit/', views.edit_blog, name="edit_blog"),
    path('blogs/<id>/delete/', views.delete_blog, name="delete_blog"),
]