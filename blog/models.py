from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
from account.models import Profile

# Create your models here.

class BlogCategory(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="blog_categories_created", null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class Tag(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="blog_tags", null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
    
class Blog(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="blogs_created", null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.DO_NOTHING, related_name="blogs", null=True, blank=True)
    post = HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to="blogs/images/", null=True, blank=True)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name="blogs")
    status = models.CharField(max_length=100, default="Draft", choices=(("Draft", "Draft"),("Published", "Published")))
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created']

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=150)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.comment
    class Meta:
        ordering = ['date']