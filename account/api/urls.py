from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('blogs', views.BlogViewSet)
router.register('site', views.SiteViewSet)
router.register('templates', views.TemplateViewSet)
router.register('messages', views.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]