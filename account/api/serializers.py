from rest_framework import serializers
from account.models import *
from blog.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user','firstName', 'lastName', 'email', 'phone_number', 'api_key', 'image',
        'about', 'is_premium_user']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'firstName', 'lastName', 'image']

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'title', 'image']

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'title', 'slug', 'tagline', 'description', 'about',
        'logo', 'icon', 'template']

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'title', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title', 'slug']

class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)
    category = BlogCategorySerializer(many=False, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'category', 'image', 'featured',
        'status', 'author', 'post','tags', 'created']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'comment', 'date', 'active']