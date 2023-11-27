from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.admin_login, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('index/', views.index, name="index"),
    path('pricing/', views.pricing, name="pricing"),
    path('site/create/', views.create_site, name="create_site"),
    path('site/<slug>/edit/', views.edit_site, name="edit_site"),
    path('templates/', views.template_list, name="template_list"),
    path('blogs/<slug>/', views.blog_list, name="blog_list"),
    path('<slug>/blogs/add/', views.add_blog, name="add_blog"),
    path('<slug>/blogs/<id>/edit/', views.edit_blog, name="edit_blog"),
    path('<slug>/blogs/<id>/delete/', views.delete_blog, name="delete_blog"),
    path('blog_categories/', views.blog_category_list, name="blog_category_list"),
    path('blog_categories/<id>/delete/', views.delete_blog_category, name="delete_blog_category"),
    path('blog_tags/', views.blog_tag_list, name="blog_tag_list"),
    path('blog_tags/<id>/delete/', views.delete_blog_tag, name="delete_blog_tag"),
    path('site/<slug>/messages/', views.message_list, name="message_list"),
    path('site/<slug>/messages/<id>/edit/', views.edit_message, name="edit_message"),
    path('site/<slug>/messages/<id>/delete/', views.delete_message, name="delete_message"),
    path('<slug>/blogs/<id>/comments/', views.comment_list, name="comment_list"),
    path('<slug>/blogs/<blog_id>/comments/<id>/edit/', views.edit_comment, name="edit_comment"),
    path('<slug>/blogs/<blog_id>/comments/<id>/delete/', views.delete_comment, name="delete_comment"),
]