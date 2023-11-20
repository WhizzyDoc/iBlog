from rest_framework import generics, viewsets
from account.models import *
from blog.models import *
from .serializers import *
from account.utils import *
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.decorators import action
from django.contrib.auth import login, authenticate, logout
import secrets
import re
import json
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
import random
import decimal
import math
import string


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False,
            methods=['get'])
    def get_blogs(self, request, *args, **kwargs):
        page = self.request.query_params.get('page')
        per_page = self.request.query_params.get('per_page')
        query = self.request.query_params.get('search')
        status = self.request.query_params.get('status')
        featured = self.request.query_params.get('featured')
        profile = Profile.objects.get(user=request.user)
        try:
            if page is None:
                page = 1
            else:
                page = int(page)
            if per_page is None:
                per_page = 20
            else:
                per_page = int(per_page)
            if query is None:
                query = ""
            start = (page - 1) * per_page
            stop = page * per_page
            total_items = 0
            blogs = None
            feat = None
            if status == 'all' and featured == 'all':
                total_items = Blog.objects.filter(author=profile).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).count()
                blogs = Blog.objects.filter(author=profile).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query))[start:stop]
            elif status != 'all' and featured == 'all':
                total_items = Blog.objects.filter(author=profile, status=status).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).count()
                blogs = Blog.objects.filter(author=profile, status=status).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query))[start:stop]
            elif status == 'all' and featured != 'all':
                if featured.lower() == 'true':
                    feat = True
                elif featured.lower() == 'false':
                    feat = False
                total_items = Blog.objects.filter(author=profile, featured=feat).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).count()
                blogs = Blog.objects.filter(author=profile, featured=feat).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query))[start:stop]
            elif status != 'all' and featured != 'all':
                if featured.lower() == 'true':
                    feat = True
                elif featured.lower() == 'false':
                    feat = False
                total_items = Blog.objects.filter(author=profile, featured=feat, status=status).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query)).count()
                blogs = Blog.objects.filter(author=profile, featured=feat, status=status).filter(Q(title__icontains=query) |
                                                Q(post__icontains=query))[start:stop]
            total_pages = math.ceil(total_items/per_page)
            if blogs.exists():
                return Response({
                    'status': 'success',
                    'data': [BlogSerializer(blog).data for blog in blogs],
                    'message': 'blog list retrieved',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'No blogs found',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "search_query": query
                })
        except:
            return Response({
                'status': 'error',
                'message': 'Error getting blog list'
            })
    @action(detail=False,
            methods=['get'])
    def get_blog_categories(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            cats = BlogCategory.objects.filter(owner=profile)
            if cats.exists():
                return Response({
                    'status': 'success',
                    'message': 'categories found',
                    'data': [BlogCategorySerializer(c).data for c in cats]
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'no category found'
                })
        except:
            return Response({
                'status': 'error',
                'message': 'error occured'
            })
    """
    @action(detail=False,
            methods=['post'])
    def create_category(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        title = request.POST.get('title')
        slug = slugify(title)
        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                # check if category does not exist
                category = NewsCategory.objects.get(slug=slug)
                if category is not None:
                    return Response({
                        'status': "error",
                        "message": "category already exists!"
                    })
                else:
                    new_cat = NewsCategory(title=title, slug=slug)
                    new_cat.save()
                    Log.objects.create(user=profile, action=f"created a news category {title}")
                    return Response({
                        'status': "success",
                        "message": "category created sucessfully",
                        "data": NewsCategorySerializer(new_cat).data,
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "Invalid API token"
            })
    @action(detail=False,
            methods=['post'])
    def edit_category(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        title = request.POST.get('title')
        slug = slugify(title)
        id = int(request.POST.get('id'))
        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                try:
                    category = NewsCategory.objects.get(id=id)
                    category.title = title
                    category.slug = slug
                    category.save()
                    Log.objects.create(user=profile, action=f"edited news category {category.title}")
                    return Response({
                        'status': "success",
                        "message": "category edited sucessfully",
                        "data": NewsCategorySerializer(category).data,
                    })
                except:
                    return Response({
                        "status": "error",
                        "message": f"category  with id \'{id}\' does not exist"
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "invalid API token"
            })
    @action(detail=False,
            methods=['post'])
    def delete_category(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        id = int(request.POST.get('id'))
        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                try:
                    category = NewsCategory.objects.get(id=id)
                    category.delete()
                    Log.objects.create(user=profile, action=f"deleted category {category.title}")
                    return Response({
                        'status': "success",
                        "message": f"category \'{category.title}\' deleted sucessfully",
                    })
                except:
                    return Response({
                        "status": "error",
                        "message": f"category  with id \'{id}\' does not exist"
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "Invalid API token"
            })

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False,
            methods=['get'])
    def filter_news(self, request, *args, **kwargs):
        page = self.request.query_params.get('page')
        per_page = self.request.query_params.get('per_page')
        active_filter = self.request.query_params.get('active')
        verify_filter = self.request.query_params.get('verified')
        #cat_filter = self.request.query_params.get('category_id')
        try:
            if page is None:
                page = 1
            else:
                page = int(page)
            if per_page is None:
                per_page = 20
            else:
                per_page = int(per_page)
            if active_filter is None:
                active_filter = True
            elif active_filter.lower() == 'true':
                active_filter = True
            elif active_filter.lower() == 'false':
                active_filter = False
            else:
                active_filter = True
            if verify_filter is None:
                verify_filter = True
            elif verify_filter.lower() == 'true':
                verify_filter = True
            elif verify_filter.lower() == 'false':
                verify_filter = False
            else:
                verify_filter = True
            start = (page - 1) * per_page
            stop = page * per_page
            total_items = News.objects.filter(active=active_filter, verified=verify_filter).count()
            total_pages = math.ceil(total_items/per_page)
            news = News.objects.filter(active=active_filter, verified=verify_filter)[start:stop]
            if news.exists():
                return Response({
                    'status': 'success',
                    'data': [NewsSerializer(ne).data for ne in news],
                    'message': 'news list retrieved',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items
                })
            else:
                return Response({
                    'status': 'success',
                    'message': 'No news found',
                    'page_number': page,
                    "list_per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items
                })
        except:
            return Response({
                'status': 'error',
                'message': 'Error getting news list'
            })
    @action(detail=False,
        methods=['get'])
    def get_news(self, request, *args, **kwargs):
        id = self.request.query_params.get('news_id')
        if id:
            try:
                news = News.objects.get(id=int(id))
                if news is not None:
                    return Response({
                        'status': 'success',
                        'data': NewsSerializer(news).data,
                        'message': 'news details retrieved'
                    })
                else:
                    return Response({
                        'status': 'success',
                        'message': 'Invalid news ID'
                    })
            except:
                return Response({
                    'status': 'error',
                    'message': 'Invalid news ID'
                })
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid news ID'
            })
    @action(detail=False,
            methods=['post'])
    def create_news(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        title = request.POST.get('title')
        slug = slugify(title)
        post = request.POST.get('post')
        active = request.POST.get('active')
        verified = request.POST.get('verified')
        cat_id = int(request.POST.get('category_id'))
        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                try:
                    category = NewsCategory.objects.get(id=cat_id)
                    try:
                        news = News(author=profile, title=title, slug=slug, post=post,
                                        category=category, active=active, verified=verified)
                        news.save()
                        Log.objects.create(user=profile, action=f"created a new post {title}")
                        create_action(profile, "added a news post", news)
                        return Response({
                            'status': "success",
                            "message": "news created sucessfully",
                            "data": NewsSerializer(news).data,
                        })
                    except:
                        return Response({
                            'status': "error",
                            "message": "error while creating news"
                        })
                except:
                    return Response({
                        "status": "error",
                        "message": f"category with id \'{id}\' does not exist"
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "invalid API token"
            })

    @action(detail=False,
            methods=['post'])
    def edit_news(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        id = int(request.POST.get('news_id'))
        title = request.POST.get('title')
        post = request.POST.get('post')
        active = request.POST.get('active')
        verified = request.POST.get('verified')
        cat_id = int(request.POST.get('category_id'))

        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                try:
                    news = News.objects.get(id=id)
                    try:
                        if cat_id:
                            try:
                                category = NewsCategory.objects.get(id=cat_id)
                                news.category = category
                                news.save()
                            except:
                                return Response({
                                    "status": "error",
                                    "message": f"category  with id \'{id}\' does not exist"
                                })
                        if title:
                            news.title = title
                            slug = slugify(title)
                            news.slug = slug
                            news.save()
                        if post:
                            news.post = post
                            news.save()
                        if active:
                            news.active = active
                            news.save()
                        if verified:
                            news.verified = verified
                            news.save()
                        Log.objects.create(user=profile, action=f"edited a news post {title}")
                        return Response({
                            'status': "success",
                            "message": f"\'{news.title}\' edited sucessfully",
                            "data": NewsSerializer(news).data,
                        })
                    except:
                        return Response({
                            'status': "error",
                            "message": "error while saving news"
                        })
                except:
                    return Response({
                        'status': "error",
                        "message": "invalid news id"
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "invalid API token"
            })
    @action(detail=False,
            methods=['post'])
    def delete_news(self, request, *args, **kwargs):
        key = request.POST.get('api_token')
        id = int(request.POST.get('id'))
        try:
            profile = Profile.objects.get(api_token=key)
            user = profile.user
            if admin_group in user.groups.all():
                try:
                    news = News.objects.get(id=id)
                    news.delete()
                    Log.objects.create(user=profile, action=f"deleted a news post {news.title}")
                    return Response({
                        'status': "success",
                        "message": f"news \'{news.title}\' deleted sucessfully",
                    })
                except:
                    return Response({
                        "status": "error",
                        "message": f"news with id \'{id}\' does not exist"
                    })
            else:
                return Response({
                    'status': "error",
                    "message": "User is not authorized"
                })
        except:
            return Response({
                'status': "error",
                "message": "Invalid API token"
            })
    """