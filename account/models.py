from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField

# Create your models here.
class TemplateCategory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class Plan(models.Model):
    title = models.CharField(max_length=200)
    price = models.BigIntegerField(default=0)
    site_number = models.IntegerField(default=1)
    level = models.PositiveIntegerField(default=0)
    domain = models.BooleanField(default=False)
    ecommerce = models.BooleanField(default=False)
    user_support = models.BooleanField(default=False)
    template_editing = models.BooleanField(default=False)
    ai_assistant = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['level','id']

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    firstName = models.CharField(max_length=100, verbose_name="First Name", null=True)
    lastName = models.CharField(max_length=100, verbose_name="Last Name", null=True)
    email = models.EmailField(max_length=200, verbose_name="Email", null=True, blank=True)
    phone_number = models.CharField(max_length=200, verbose_name="Phone Number", null=True, blank=True)
    api_key = models.CharField(max_length=1000, verbose_name="API Key", null=True, blank=True)
    image = models.ImageField(upload_to="users/images/", blank=True, null=True)
    about = HTMLField(blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, related_name="plan_users", null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    x_account = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        ordering = ['firstName']

class Developer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="developer")
    firstName = models.CharField(max_length=100, verbose_name="First Name", null=True)
    lastName = models.CharField(max_length=100, verbose_name="Last Name", null=True)
    email = models.EmailField(max_length=200, verbose_name="Email", null=True, blank=True)
    phone_number = models.CharField(max_length=200, verbose_name="Phone Number", null=True, blank=True)
    api_key = models.CharField(max_length=1000, verbose_name="API Key", null=True, blank=True)
    image = models.ImageField(upload_to="developers/images/", blank=True, null=True)
    about = HTMLField(blank=True, null=True)
    github = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    x_account = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.user.__str__()

    class Meta:
        ordering = ['firstName']
        
class Template(models.Model):
    owner = models.ForeignKey(Developer, on_delete=models.SET_NULL, related_name="profile", null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(TemplateCategory, on_delete=models.SET_NULL, related_name="category_templates", null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, related_name="plan_templates", null=True, blank=True)
    description = HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to="template/image/", null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class MainSite(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="main_site")
    title = models.CharField(null=True, blank=True, max_length=100)
    tagline = models.CharField(null=True, blank=True, max_length=250)
    description = models.TextField(null=True, blank=True)
    about = HTMLField(null=True, blank=True)
    logo = models.ImageField(upload_to="iblog/logo/", null=True, blank=True)
    icon = models.ImageField(upload_to="iblog/icon/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
        
class Site(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="site")
    title = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    tagline = models.CharField(null=True, blank=True, max_length=250)
    description = models.TextField(null=True, blank=True)
    about = HTMLField(null=True, blank=True)
    logo = models.ImageField(upload_to="site/logo/", null=True, blank=True)
    icon = models.ImageField(upload_to="site/icon/", null=True, blank=True)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, related_name="sites", null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class Contact(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="messages")
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()
    reply = HTMLField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.message
    class Meta:
        ordering = ['-date']

class Notification(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=150)
    note = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-date']
