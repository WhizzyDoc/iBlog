from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    firstName = models.CharField(max_length=100, verbose_name="First Name", null=True)
    lastName = models.CharField(max_length=100, verbose_name="Last Name", null=True)
    email = models.EmailField(max_length=200, verbose_name="Email", null=True, blank=True)
    phone_number = models.CharField(max_length=200, verbose_name="Phone Number", null=True, blank=True)
    api_key = models.CharField(max_length=1000, verbose_name="API Key", null=True, blank=True)
    image = models.ImageField(upload_to="users/images/", blank=True, null=True)
    about = HTMLField()
    is_premium_user = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        ordering = ['firstName']
        
class Template(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="template/image/", null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
        
class Site(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="site")
    title = models.CharField(null=True, blank=True, max_length=100)
    tagline = models.CharField(null=True, blank=True, max_length=250)
    description = models.TextField(null=True, blank=True)
    about = HTMLField(null=True, blank=True)
    logo = models.ImageField(upload_to="site/logo/", null=True, blank=True)
    icon = models.ImageField(upload_to="site/icon/", null=True, blank=True)
    template = models.ForeignKey(Template, on_delete=models.DO_NOTHING, related_name="sites", null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
