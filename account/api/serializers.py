from rest_framework import serializers
from ..models import *
from blog.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',]

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'title', 'price', 'site_number', 'domain',
                  'ecommerce', 'user_support', 'template_editing',
                  'ai_assistant', 'level']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'user','firstName', 'lastName', 'email', 'phone_number', 'api_key', 'image',
        'about']

class DeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Developer
        fields = ['id', 'user','firstName', 'lastName', 'email', 'phone_number', 'api_key', 'image',
        'about', 'github', 'facebook', 'linkedin', 'x_account']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'firstName', 'lastName', 'image']

class TemplateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateCategory
        fields = ['id', 'title', 'slug']

class TemplateSerializer(serializers.ModelSerializer):
    owner = DeveloperSerializer(many=False, read_only=True)
    category = TemplateCategorySerializer(many=False, read_only=True)
    plan = PlanSerializer(many=False, read_only=True)
    class Meta:
        model = Template
        fields = ['id', 'title', 'image', 'description', 'category',
                  'owner', 'plan']

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
        fields = ['id', 'title', 'slug', 'category', 'image',
        'status', 'author', 'post','tags', 'created', 'meta_keywords', 'meta_description']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'comment', 'reply', 'date', 'active']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'reply', 'date']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'note', 'date']