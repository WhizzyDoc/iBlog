from rest_framework import serializers
from blog.models import *
from account.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user','firstName', 'lastName', 'email', 'phone_number', 'image',
                  'about', 'is_premium_user', 'api_key']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'firstName', 'lastName', 'email', 'phone_number', 'image']

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'title','image']

class SiteSerializer(serializers.ModelSerializer):
    template = TemplateSerializer(many=False, read_only=True)
    class Meta:
        model = Site
        fields = ['id', 'title', 'tagline', 'description', 'logo', 'about', 'icon', 'template']

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'title', 'slug']

class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)
    category = BlogCategorySerializer(many=False, read_only=True)
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'author', 'category', 'image', 'status', 'post', 'created']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'comment', 'date']

